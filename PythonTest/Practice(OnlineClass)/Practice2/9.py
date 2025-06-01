scores = eval(input())
fail_scores = [s for s in scores if s < 60]
excellent_scores = [s for s in scores if s >= 90]
fail_avg = sum(fail_scores) / len(fail_scores) if fail_scores else 0
excellent_avg = sum(excellent_scores) / len(excellent_scores) if excellent_scores else 0
print(f"{fail_avg:.1f}")
print(f"{excellent_avg:.1f}")