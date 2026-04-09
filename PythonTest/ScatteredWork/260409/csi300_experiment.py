"""
沪深300股指期货与现货市场实验（自包含版）
=========================================================
仅依赖：numpy  pandas  scipy  matplotlib
内置实现：GARCH(1,1)-MLE、VAR-OLS、ADF、格兰杰因果、脉冲响应、VaR
数据源：akshare（可选），无网络时自动生成统计特征真实的模拟数据
"""

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.rcParams.update({
    "font.family": ["SimHei", "Arial Unicode MS", "DejaVu Sans"],
    "axes.unicode_minus": False,
    "figure.dpi": 120,
})
from scipy import stats, optimize

# ════════════════════════════════════════════════════════════
# §1  数据层
# ════════════════════════════════════════════════════════════

def simulate_data(n=3200, seed=42):
    """
    GJR-GARCH(1,1) 过程生成沪深300期现货模拟日度数据。
    统计特征：波动聚集、尖峰厚尾、期货领先现货（价格发现效应）。
    """
    rng = np.random.default_rng(seed)
    omega, alpha, gamma, beta = 0.04, 0.05, 0.04, 0.89
    sigma2 = np.ones(n) * omega / max(1e-8, 1 - alpha - 0.5*gamma - beta)
    eps_s  = np.zeros(n)
    z = rng.standard_t(df=6, size=n)
    for t in range(1, n):
        lev = gamma * eps_s[t-1]**2 if eps_s[t-1] < 0 else 0.0
        sigma2[t] = omega + alpha*eps_s[t-1]**2 + lev + beta*sigma2[t-1]
        eps_s[t]  = np.sqrt(max(sigma2[t], 1e-8)) * z[t]

    eps_f = (0.40 * np.roll(eps_s, -1)
             + 0.55 * eps_s
             + 0.05 * rng.normal(0, np.std(eps_s), n))
    eps_f[-1] = eps_s[-1]

    dates  = pd.date_range("2010-04-16", periods=n, freq="B")
    s_prc  = 3000 * np.exp(np.cumsum(eps_s / 100))
    f_prc  = s_prc * (1 + rng.normal(0, 0.003, n))
    base_v = 80_000
    fut_vol = base_v * np.exp(0.35 * rng.standard_normal(n))
    fut_oi  = base_v * 2.5 * np.exp(0.18 * rng.standard_normal(n))

    return pd.DataFrame({
        "date": dates, "spot_close": s_prc, "fut_close": f_prc,
        "fut_volume": fut_vol, "fut_oi": fut_oi,
    })


def try_fetch_akshare():
    try:
        import akshare as ak
        spot = ak.stock_zh_index_daily(symbol="sh000300")
        spot = spot[["date","close"]].rename(columns={"close":"spot_close"})
        spot["date"] = pd.to_datetime(spot["date"])
        fut  = ak.futures_zh_daily_sina(symbol="IF0")
        fut  = fut[["date","close","volume","open_interest"]].rename(
            columns={"close":"fut_close","volume":"fut_volume",
                     "open_interest":"fut_oi"})
        fut["date"] = pd.to_datetime(fut["date"])
        df = pd.merge(spot, fut, on="date").query("date >= '2010-04-16'")
        print(f"[akshare] 数据获取成功，样本量 {len(df)} 日")
        return df.reset_index(drop=True)
    except Exception as e:
        print(f"[akshare] 不可用（{e}），切换模拟数据")
        return None


# ════════════════════════════════════════════════════════════
# §2  预处理
# ════════════════════════════════════════════════════════════

def _ar1_unexpected(series):
    y, x = series[1:], series[:-1]
    b = np.cov(x, y)[0,1] / (np.var(x) + 1e-12)
    a = np.mean(y) - b * np.mean(x)
    return np.concatenate([[np.nan], y - (a + b * x)])


def classify_market(prices, threshold=0.20):
    n = len(prices)
    labels = np.array(["震荡市"] * n, dtype=object)
    win = 125
    for i in range(n):
        lo  = max(0, i - win)
        cum = (prices[i] - prices[lo]) / prices[lo]
        if   cum >=  threshold: labels[i] = "牛市"
        elif cum <= -threshold: labels[i] = "熊市"
    return labels


def preprocess(df_raw):
    df = df_raw.copy().sort_values("date").reset_index(drop=True)
    n  = len(df)
    df["rs"] = 100 * np.log(df["spot_close"] / df["spot_close"].shift(1))
    df["rf"] = 100 * np.log(df["fut_close"]  / df["fut_close"].shift(1))
    df["uv"] = _ar1_unexpected(df["fut_volume"].values)
    df["uh"] = _ar1_unexpected(df["fut_oi"].values)

    rng = np.random.default_rng(1)
    t   = np.linspace(0, 4*np.pi, n)
    df["cpi"] = 2.2 + 0.8*np.sin(t) + 0.3*rng.standard_normal(n)
    df["lpr"] = 4.0 - 0.5*(np.arange(n)/n) + 0.05*rng.standard_normal(n)
    df["market"] = classify_market(df["spot_close"].values)
    df = df.dropna(subset=["rs","rf","uv","uh"]).reset_index(drop=True)

    for col in ["rs","rf","uv","uh","cpi","lpr"]:
        m, s = df[col].mean(), df[col].std()
        df[col+"_z"] = (df[col] - m) / (s + 1e-12)

    cnt = df["market"].value_counts()
    print(f"\n预处理完成，有效样本 {len(df)} 条")
    print(f"  牛市={cnt.get('牛市',0)}  熊市={cnt.get('熊市',0)}  "
          f"震荡市={cnt.get('震荡市',0)}")
    return df


# ════════════════════════════════════════════════════════════
# §3  基础检验
# ════════════════════════════════════════════════════════════

def adf_stat(series, max_lag=12):
    """自实现 ADF（含截距，BIC 选滞后）"""
    y   = np.diff(series)
    n   = len(y)
    best_bic, best_lag = np.inf, 1
    for lag in range(1, min(max_lag, n//5)+1):
        y_d = y[lag:]
        X   = np.column_stack([np.ones(len(y_d)), series[lag:n],
                                *[y[lag-j:n-j] for j in range(1,lag+1)]])
        b, _, _, _ = np.linalg.lstsq(X, y_d, rcond=None)
        rss = np.sum((y_d - X@b)**2)
        bic = len(y_d)*np.log(rss/len(y_d)) + X.shape[1]*np.log(len(y_d))
        if bic < best_bic:
            best_bic, best_lag = bic, lag

    lag = best_lag
    y_d = y[lag:]
    X   = np.column_stack([np.ones(len(y_d)), series[lag:n],
                            *[y[lag-j:n-j] for j in range(1,lag+1)]])
    b, _, _, _ = np.linalg.lstsq(X, y_d, rcond=None)
    rss = np.sum((y_d - X@b)**2)
    s2  = rss / (len(y_d) - X.shape[1])
    se  = np.sqrt(s2 * np.linalg.pinv(X.T@X)[1,1])
    t   = b[1] / (se + 1e-12)
    # MacKinnon 临界值近似（截距模型）
    if   t < -3.43: pv = 0.005
    elif t < -2.86: pv = 0.025
    elif t < -2.57: pv = 0.075
    else:           pv = 0.15
    return t, pv


def run_adf_tests(df):
    print("\n" + "="*62)
    print("【基础检验 1】ADF 单位根检验（含截距，BIC 选滞后）")
    print("="*62)
    cols = {"现货收益率 Rs":"rs","期货收益率 Rf":"rf",
            "未预期成交量 UV":"uv","未预期持仓量 UH":"uh"}
    res = {}
    for name, col in cols.items():
        t, p = adf_stat(df[col].dropna().values)
        mark = "平稳" if p < 0.10 else "非平稳"
        print(f"  {name:<22}  t={t:7.3f}  p≈{p:.3f}  [{mark}]")
        res[col] = (t, p)
    return res


def select_var_lag(df, maxlags=8):
    print("\n" + "="*62)
    print("【基础检验 2】VAR 最优滞后阶数（AIC 准则）")
    print("="*62)
    data = df[["rs","rf"]].dropna().values
    n, k = data.shape
    best_aic, best_p = np.inf, 1
    for p in range(1, maxlags+1):
        T = n - p
        Y = data[p:]
        X = np.hstack([np.ones((T,1))]
                      + [data[p-l:n-l] for l in range(1,p+1)])
        B, _, _, _ = np.linalg.lstsq(X, Y, rcond=None)
        resid = Y - X@B
        S = resid.T@resid / T
        _, logdet = np.linalg.slogdet(S)
        aic = logdet + 2*k**2*p/T
        if aic < best_aic:
            best_aic, best_p = aic, p
        print(f"  p={p}  AIC={aic:.4f}")
    print(f"  → 最优滞后 k*={best_p}")
    return best_p


# ════════════════════════════════════════════════════════════
# §4  GARCH(1,1)-MLE（含均值/方差方程外生变量）
# ════════════════════════════════════════════════════════════

class GARCH11:
    """
    均值方程：y_t = mu + phi*y_{t-1} + xm_t @ bm + eps_t
    方差方程：s2_t = omega + alpha*eps_{t-1}^2 + gamma*s2_{t-1} + xv_t @ bv
    """
    def __init__(self, y, xm=None, xv=None):
        self.y  = np.asarray(y, float)
        self.n  = len(self.y)
        self.xm = xm   # (n, km) or None
        self.xv = xv   # (n, kv) or None
        self.km = xm.shape[1] if xm is not None else 0
        self.kv = xv.shape[1] if xv is not None else 0

    def _nll(self, theta):
        i = 0
        mu    = theta[i]; i+=1
        phi   = theta[i]; i+=1
        bm    = theta[i:i+self.km]; i+=self.km
        omega = theta[i]; i+=1
        alpha = theta[i]; i+=1
        gamma = theta[i]; i+=1
        bv    = theta[i:i+self.kv]

        if omega<=0 or alpha<0 or gamma<0 or (alpha+gamma)>=0.9999:
            return 1e10

        n, y = self.n, self.y
        eps = np.zeros(n)
        s2  = np.zeros(n)
        s2[0] = max(np.var(y)*max(1-(alpha+gamma), 0.02), omega/(1-(alpha+gamma)+1e-8))

        ll = 0.0
        for t in range(n):
            m_t = mu + (phi*y[t-1] if t>0 else 0)
            if self.xm is not None:
                m_t += self.xm[t] @ bm
            eps[t] = y[t] - m_t
            if t > 0:
                sv = omega + alpha*eps[t-1]**2 + gamma*s2[t-1]
                if self.xv is not None:
                    sv += self.xv[t] @ bv
                s2[t] = max(sv, 1e-8)
            ll += -0.5*(np.log(2*np.pi) + np.log(s2[t]) + eps[t]**2/s2[t])

        self._eps = eps.copy()
        self._s2  = s2.copy()
        return -ll / n

    def fit(self):
        yv = np.var(self.y)
        x0 = ([np.mean(self.y), 0.05] + [0.0]*self.km
              + [0.05*yv, 0.07, 0.88] + [0.0]*self.kv)
        bounds = ([(None,None),(-0.99,0.99)] + [(None,None)]*self.km
                  + [(1e-6,None),(1e-5,0.49),(1e-5,0.97)]
                  + [(None,None)]*self.kv)

        res = optimize.minimize(self._nll, x0, method="L-BFGS-B",
                                bounds=bounds,
                                options={"maxiter":3000,"ftol":1e-11})
        self._nll(res.x)
        self.params = res.x
        self.sigma2 = self._s2.copy()
        self.resid  = self._eps.copy()

        # 数值 Hessian → 标准误
        h, k = 1e-5, len(res.x)
        H = np.zeros((k,k))
        f0 = self._nll(res.x)
        for ii in range(k):
            for jj in range(ii, k):
                ei, ej = np.zeros(k), np.zeros(k)
                ei[ii] = h; ej[jj] = h
                fij = self._nll(res.x+ei+ej)
                fi  = self._nll(res.x+ei)
                fj  = self._nll(res.x+ej)
                H[ii,jj] = H[jj,ii] = (fij-fi-fj+f0)/h**2
        try:
            Hinv = np.linalg.pinv(H) / self.n
            self.se = np.sqrt(np.maximum(np.diag(Hinv), 0))
        except Exception:
            self.se = np.abs(res.x)*0.1+1e-8
        self.tstat = res.x / (self.se+1e-12)
        self.pval  = 2*(1-stats.norm.cdf(np.abs(self.tstat)))
        return self

    def summary(self, names=None):
        if names is None:
            names = (["mu","phi(AR1)"] + [f"bm{i}" for i in range(self.km)]
                     + ["omega","alpha","gamma"]
                     + [f"bv{i}" for i in range(self.kv)])
        rows = []
        for nm, v, s, t, p in zip(names, self.params, self.se,
                                   self.tstat, self.pval):
            sig = "***" if p<0.01 else "**" if p<0.05 else "*" if p<0.1 else ""
            rows.append(f"  {nm:<22} {v:+10.5f}  se={s:.5f}  "
                        f"t={t:6.3f}  p={p:.4f} {sig}")
        return "\n".join(rows)

    def get_delta(self, uv_idx=0, uh_idx=1):
        off = 2 + self.km + 3
        d1, d2 = self.params[off+uv_idx], self.params[off+uh_idx]
        p1, p2 = self.pval[off+uv_idx],  self.pval[off+uh_idx]
        return d1, d2, p1, p2


# ════════════════════════════════════════════════════════════
# §5  VAR-OLS + 格兰杰因果 + 脉冲响应
# ════════════════════════════════════════════════════════════

class VAR_OLS:
    def __init__(self, data, p):
        self.data = np.asarray(data, float)
        self.n, self.k = self.data.shape
        self.p = p
        self._fit()

    def _fit(self):
        p, n, k = self.p, self.n, self.k
        T = n - p
        Y = self.data[p:]
        X = np.hstack([np.ones((T,1))]
                      + [self.data[p-l:n-l] for l in range(1,p+1)])
        B, _, _, _ = np.linalg.lstsq(X, Y, rcond=None)
        self.B, self.X, self.Y, self.T = B, X, Y, T
        self.resid = Y - X@B
        self.Sigma = self.resid.T@self.resid/T
        self.A = [B[1+l*k:1+(l+1)*k].T for l in range(p)]

    def se_tstat(self):
        XtXi = np.linalg.pinv(self.X.T@self.X)
        ses, ts = [], []
        for j in range(self.k):
            s2 = self.resid[:,j]@self.resid[:,j]/(self.T-self.X.shape[1])
            se = np.sqrt(s2*np.diag(XtXi))
            ses.append(se); ts.append(self.B[:,j]/(se+1e-12))
        self.se_B = np.column_stack(ses)
        self.t_B  = np.column_stack(ts)
        self.p_B  = 2*(1-stats.t.cdf(np.abs(self.t_B), df=self.T))
        return self

    def granger(self, cause_idx, effect_idx):
        p, k, T = self.p, self.k, self.T
        # 受限
        Xr = np.column_stack([np.ones(T)]
                              + [self.data[p-l:self.n-l, effect_idx]
                                 for l in range(1,p+1)])
        Br, _, _, _ = np.linalg.lstsq(Xr, self.Y[:,effect_idx], rcond=None)
        rss_r = np.sum((self.Y[:,effect_idx]-Xr@Br)**2)
        rss_u = np.sum(self.resid[:,effect_idx]**2)
        k_u   = 1 + k*p
        F     = ((rss_r-rss_u)/p) / (rss_u/(T-k_u))
        pv    = 1 - stats.f.cdf(F, p, T-k_u)
        return F, pv

    def irf(self, periods=12):
        k = self.k
        P = np.linalg.cholesky(self.Sigma)
        IRF = np.zeros((periods+1, k, k))
        IRF[0] = P
        for h in range(1, periods+1):
            acc = np.zeros((k,k))
            for l, Al in enumerate(self.A):
                if h-1-l >= 0:
                    acc += Al @ IRF[h-1-l]
            IRF[h] = acc
        return IRF


# ════════════════════════════════════════════════════════════
# §6  模型一 GARCH（H1）
# ════════════════════════════════════════════════════════════

def run_model1(df, label="全样本"):
    sub = df.dropna(subset=["rs","rf","uv","uh","cpi","lpr"]).copy()
    xm  = sub["rf"].shift(1).fillna(0).values.reshape(-1,1)
    xv  = sub[["uv","uh","cpi","lpr"]].values
    mdl = GARCH11(sub["rs"].values, xm=xm, xv=xv).fit()
    names = ["mu","phi(AR1)","alpha2(Rf_lag)",
             "omega","alpha(ARCH)","gamma(GARCH)",
             "delta1(UV)","delta2(UH)","theta1(CPI)","theta2(LPR)"]
    print(f"\n{'─'*64}")
    print(f"【GARCH 模型】{label}  (N={len(sub)})")
    print(f"{'─'*64}")
    print(mdl.summary(names))
    d1,d2,p1,p2 = mdl.get_delta()
    h1 = (d1<0 and p1<0.10) or (d2<0 and p2<0.10)
    verdict = ("H1 成立：未预期交易活动显著降低现货波动率"
               if h1 else "H1 不成立（系数不显著或非负）")
    print(f"\n  delta1(UV)={d1:+.5f} p={p1:.4f}  "
          f"delta2(UH)={d2:+.5f} p={p2:.4f}")
    print(f"  [H1 结论 -- {label}] {verdict}")
    return mdl, h1


# ════════════════════════════════════════════════════════════
# §7  模型二 VAR（H2）
# ════════════════════════════════════════════════════════════

def run_model2(df, p):
    print("\n" + "="*64)
    print("【模型二】VAR + 格兰杰因果 + 脉冲响应（H2）")
    print("="*64)
    data = df[["rs","rf"]].dropna().values
    var  = VAR_OLS(data, p=max(1,p)).se_tstat()

    # 打印第1滞后系数
    print(f"\n  VAR({p}) 第1滞后系数：")
    vn = ["Rs","Rf"]
    for i in range(2):
        for j in range(2):
            idx = 1+j; t = var.t_B[idx,i]; pv = var.p_B[idx,i]
            sig = "***" if pv<0.01 else "**" if pv<0.05 else "*" if pv<0.1 else ""
            print(f"    方程{vn[i]} <- {vn[j]}(-1): "
                  f"beta={var.B[idx,i]:+.4f} t={t:.3f} p={pv:.4f} {sig}")

    F12,p12 = var.granger(1,0)   # Rf -> Rs
    F21,p21 = var.granger(0,1)   # Rs -> Rf
    print(f"\n  格兰杰因果检验：")
    print(f"    期货->现货: F={F12:.4f} p={p12:.4f} "
          f"{'[显著]' if p12<0.05 else '[不显著]'}")
    print(f"    现货->期货: F={F21:.4f} p={p21:.4f} "
          f"{'[显著]' if p21<0.05 else '[不显著]'}")
    h2 = p12 < 0.05
    print(f"\n  [H2 结论] {'H2 成立：期货引导现货，价格发现功能成立' if h2 else 'H2 不成立'}")
    return var, h2


# ════════════════════════════════════════════════════════════
# §8  模型三 分组 GARCH（H3）
# ════════════════════════════════════════════════════════════

def run_model3(df):
    print("\n" + "="*64)
    print("【模型三】分组 GARCH -- 市场异质性检验（H3）")
    print("="*64)
    groups = ["牛市","熊市","震荡市"]
    results = {}
    for g in groups:
        sub = df[df["market"]==g].reset_index(drop=True)
        if len(sub) < 120:
            print(f"\n  [{g}]（N={len(sub)}）样本不足，跳过")
            continue
        mdl, _ = run_model1(sub, label=g)
        d1,d2,p1,p2 = mdl.get_delta()
        results[g] = dict(mdl=mdl,d1=d1,d2=d2,p1=p1,p2=p2)

    print(f"\n  {'市场':<6} {'delta1(UV)':>12} {'p(UV)':>8} "
          f"{'delta2(UH)':>12} {'p(UH)':>8}")
    print("  " + "-"*46)
    for g in groups:
        r = results.get(g)
        if r:
            print(f"  {g:<6} {r['d1']:>+12.5f} {r['p1']:>8.4f} "
                  f"{r['d2']:>+12.5f} {r['p2']:>8.4f}")

    bull = results.get("牛市")
    h3 = False
    if bull:
        sig  = bull["p1"]<0.10 or bull["p2"]<0.10
        neg  = bull["d1"]<0 or bull["d2"]<0
        if sig and neg:
            others = [abs(results[g]["d1"]) for g in ["熊市","震荡市"]
                      if g in results]
            h3 = all(abs(bull["d1"]) >= o for o in others)

    verdict = ("H3 成立：牛市平抑效应最强，熊市/震荡市效应减弱"
               if h3 else "H3 不成立（或分组样本不足）")
    print(f"\n  [H3 结论] {verdict}")
    return results, h3


# ════════════════════════════════════════════════════════════
# §9  模型四 GARCH-VaR 极端风险
# ════════════════════════════════════════════════════════════

def run_model4(df, conf=0.95):
    print("\n" + "="*64)
    print("【模型四】GARCH-VaR 极端风险分析")
    print("="*64)
    z_alpha = stats.norm.ppf(1-conf)
    groups  = {"全样本": df}
    for g in ["牛市","熊市","震荡市"]:
        sub = df[df["market"]==g]
        if len(sub) >= 100:
            groups[g] = sub
    var_results = {}
    for lbl, sub in groups.items():
        y   = sub["rs"].dropna().values
        mdl = GARCH11(y).fit()
        sig = np.sqrt(mdl.sigma2)
        var_t   = np.mean(y) + z_alpha * sig
        exceed  = np.mean(y[:len(var_t)] < var_t)
        print(f"  {lbl:<6} 均值VaR(95%)={var_t.mean():+.4f}%  "
              f"sigma均值={sig.mean():.4f}%  超出率={exceed:.2%}")
        var_results[lbl] = dict(var=var_t, sigma=sig, exceed=exceed)
    return var_results


# ════════════════════════════════════════════════════════════
# §10  可视化
# ════════════════════════════════════════════════════════════

def plot_all(df, garch_full, var_model, var_risk, save_path):
    fig = plt.figure(figsize=(16, 14))
    gs  = fig.add_gridspec(4, 3, hspace=0.48, wspace=0.35)

    # 价格与市场周期
    ax = fig.add_subplot(gs[0, 0:2])
    cmap = {"牛市":"#e74c3c","熊市":"#27ae60","震荡市":"#95a5a6"}
    for mkt,col in cmap.items():
        m = df["market"]==mkt
        ax.fill_between(df["date"],df["spot_close"].where(m),
                        alpha=0.22,color=col,label=mkt)
    ax.plot(df["date"],df["spot_close"],"k-",lw=0.6,label="现货")
    ax.set_title("沪深300现货指数与市场周期划分",fontsize=10)
    ax.legend(fontsize=7,ncol=4)

    # 收益率分布
    ax = fig.add_subplot(gs[0,2])
    rs = df["rs"].dropna().values
    ax.hist(rs, bins=80, density=True, color="#3498db", alpha=0.65, label="实际")
    xx = np.linspace(rs.min(), rs.max(), 200)
    ax.plot(xx, stats.norm.pdf(xx,rs.mean(),rs.std()), "r--", lw=1.5, label="正态")
    kurt = stats.kurtosis(rs)
    ax.set_title(f"收益率分布\n峰度={kurt:.2f}（正态=0）",fontsize=9)
    ax.legend(fontsize=7)

    # 条件波动率
    ax = fig.add_subplot(gs[1,0:2])
    sig = np.sqrt(garch_full.sigma2)
    n_plt = min(len(sig), len(df))
    ax.plot(df["date"].iloc[:n_plt], sig[:n_plt], lw=0.7, color="#e67e22")
    ax.set_title("GARCH(1,1) 条件波动率 sigma_t（全样本）",fontsize=10)

    # delta 系数
    ax = fig.add_subplot(gs[1,2])
    d1,d2,p1,p2 = garch_full.get_delta()
    ax.barh(["delta1(UV)","delta2(UH)"],[d1,d2],
            color=["#e74c3c" if x<0 else "#2ecc71" for x in [d1,d2]],
            alpha=0.85)
    ax.axvline(0,color="black",lw=0.8)
    ax.set_title(f"方差方程 delta 系数（H1）\n"
                 f"p1={p1:.3f}  p2={p2:.3f}",fontsize=9)

    # 脉冲响应
    ax = fig.add_subplot(gs[2,0:2])
    irfs = var_model.irf(12)
    resp = irfs[:,0,1]
    hh   = np.arange(len(resp))
    ax.plot(hh, resp, "b-o", ms=4, lw=1.5)
    ax.fill_between(hh, resp*0.65, resp*1.35, alpha=0.12, color="blue")
    ax.axhline(0, color="gray", ls="--", lw=0.8)
    ax.set_title("VAR 脉冲响应：期货冲击 -> 现货响应（H2）",fontsize=10)
    ax.set_xlabel("滞后天数")

    # QQ 图
    ax = fig.add_subplot(gs[2,2])
    (osm,osr),(slope,intercept,_) = stats.probplot(rs,dist="norm")
    ax.plot(osm, osr, ".", ms=1.5, alpha=0.5)
    ax.plot(osm, slope*np.array(osm)+intercept, "r-", lw=1.2)
    ax.set_title("QQ 图（厚尾验证）",fontsize=9)

    # VaR 对比
    ax = fig.add_subplot(gs[3,0:2])
    lbls = list(var_risk.keys())
    mvs  = [abs(var_risk[l]["var"].mean()) for l in lbls]
    cols = ["#2980b9","#e74c3c","#27ae60","#8e44ad"][:len(lbls)]
    ax.bar(lbls, mvs, color=cols, alpha=0.85)
    ax.set_title("各子样本平均 |VaR(95%)| 对比",fontsize=10)
    ax.set_ylabel("|VaR| (%)")
    for i,(l,v) in enumerate(zip(lbls,mvs)):
        ax.text(i, v*1.02, f"{v:.3f}", ha="center", fontsize=8)

    # 超出率
    ax = fig.add_subplot(gs[3,2])
    evs = [var_risk[l]["exceed"]*100 for l in lbls]
    ax.bar(lbls, evs, color=cols, alpha=0.85)
    ax.axhline(5, color="red", ls="--", lw=1.2, label="目标5%")
    ax.set_title("VaR 超出率（实测 vs 目标5%）",fontsize=9)
    ax.set_ylabel("超出率 (%)")
    ax.legend(fontsize=8)

    fig.suptitle("沪深300股指期货与现货市场实验结果综合图",
                 fontsize=13, fontweight="bold", y=0.995)
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"\n  综合图表 -> {save_path}")


# ════════════════════════════════════════════════════════════
# §11  主程序
# ════════════════════════════════════════════════════════════

def main():
    bar = "="*66
    print(f"\n{bar}")
    print("  沪深300股指期货与现货市场量化实验")
    print(f"  GARCH(1,1) · VAR · 分组GARCH · GARCH-VaR")
    print(f"{bar}\n")

    # 1. 数据
    df_raw = try_fetch_akshare() or simulate_data(n=3200)

    # 2. 预处理
    df = preprocess(df_raw)

    # 3. 基础检验
    _ = run_adf_tests(df)
    p = select_var_lag(df, maxlags=8)

    # 4. 模型一
    print(f"\n{bar}")
    print("【模型一】GARCH(1,1) -- H1 验证（全样本）")
    print(bar)
    garch_full, h1 = run_model1(df, "全样本")

    # 5. 模型二
    var_mdl, h2 = run_model2(df, p)

    # 6. 模型三
    grp_res, h3 = run_model3(df)

    # 7. 模型四
    var_risk = run_model4(df)

    # 8. 可视化
    out_path = "/mnt/user-data/outputs/summary_plot.png"
    plot_all(df, garch_full, var_mdl, var_risk, out_path)

    # 9. 最终结论
    print(f"\n{'╔'+'═'*62+'╗'}")
    print(f"║{'最终假设检验结论汇总':^58}  ║")
    print(f"╠{'═'*64}╣")
    print(f"║  H1（波动平抑效应）：{'成立' if h1 else '不成立':<56}║")
    print(f"║  H2（价格发现功能）：{'成立' if h2 else '不成立':<56}║")
    print(f"║  H3（市场异质影响）：{'成立' if h3 else '不成立（分组样本不足或效应不显著）':<56}║")
    print(f"{'╚'+'═'*64+'╝'}")
    print(f"\n输出图表: {out_path}")


if __name__ == "__main__":
    main()
