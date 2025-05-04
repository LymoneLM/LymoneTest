using System;
using System.Collections.Generic;
using System.Linq;
using BepInEx;
using BepInEx.Logging;
using HarmonyLib;
using UnityEngine;
using System.Reflection.Emit;

namespace MeepleStationTestMod
{
    //插件描述特性 分别为 插件ID 插件名字 插件版本(必须为数字)
    [BepInPlugin("cc.lymone.plugin.meeplestation.test", "TestPlugin", "1.0")]
    public class MeepleStationTestMod : BaseUnityPlugin 
    {
        internal static new ManualLogSource Log;

        private void Start()
        {
            Log = base.Logger;
            Log.LogInfo("MeepleStationLymoneTestMod加载成功");
            
        }
        private void Awake()
        {
            new Harmony("cc.lymone.plugin.meeplestation.test").PatchAll();
        }
        [HarmonyPatch(typeof(meeple), "GetEducationBonus")]
        public class GetEducationBonusFix
        {
            public static int Away()
            {
                Log.LogInfo("GetEducationBonus Postfix has run");
                return 0;
            }
            public static void Postfix(ref int __result)
            {
                __result = 9900;
                Away();
                //MeepleStationTestMod.Log.LogInfo("GetEducationBonus Postfix has run");
            }
        }
        [HarmonyPatch(typeof(meeple), "Start")]
        public class StartFix
        {
            public static void Postfix(meeple __instance)
            {
                __instance.socialTrait = 10;
                __instance.strengthTrait = 10;
                __instance.confidenceTrait = 10;
                __instance.workEthic = 10;
                //MeepleStationTestMod.Log.LogInfo("Start Postfix has run");
            }
        }
        [HarmonyTranspiler]
        [HarmonyPatch(typeof(traderListItem), nameof(traderListItem.buyBTN))]
        public static IEnumerable<CodeInstruction> Credits(IEnumerable<CodeInstruction> instructions)
        {
            Log.LogInfo("buyBTN Patch has run");
            var codes = new List<CodeInstruction>(instructions);
            Log.LogInfo("codes[74].opcode " + codes[74].opcode);
            codes[74].opcode = OpCodes.Add;
            return codes.AsEnumerable();
        }
    }
    
    



}
