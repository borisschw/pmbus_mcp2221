#!/usr/bin/env python

import time
import RPB_Charger

print("Initializing PMBUS... \n")


rpbCharger = RPB_Charger.RPB_Charger()
time.sleep(2)

rpbCharger.rpbConfigure()
time.sleep(2)


while True:
    print("Get status")
    rpbCharger.get_status()
    print("FW version = ", "".join([chr(x) for x in rpbCharger.RPB.getMfrRevision()]))

    print(rpbCharger.last_status)
    time.sleep(5)


#     # print("Version: " + str(DRQ.getPmbusRev()))

#     # print("Tempurature: " + str(DRQ.getTempurature()))
#     # print("Input Voltage: " + str(DRQ.getVoltageIn()))

#     # DRQ.setCurve_ICHG(40)
#     # print("Curve_ICHG: " + str(DRQ.getCurve_ICHG()))


    # for i in range (14,55):
    #     try:
    #         DRQ.setCurve_ICHG(i)
    #         # DRQ.setCurve_VBST(22)
    #         # DRQ.setIOUT_OC_FAULT_LIMIT(i)
    #         # DRQ.setIoutOCLimit(i)
    #         time.sleep(3)
    #         # ICHG = DRQ.getIoutOCLimit()
    #         ICHG = DRQ.getCurve_ICHG()
    #         time.sleep(2)
    #     except Exception as e:
    #         print(str(e))
    #         continue


#         # VBST = DRQ.getCurve_VBST()
#         # print("Curve_ICHG: " + str(ICHG))
#         # # print("Curve_ICHG: " + str(VBST))
#         # print("--------->> sent: ",i)
#         # print("--------->> got: ",str(ICHG))

#         if (i == ICHG):
#             print("Success")
#         else:
#             print("----------------------------------->> Fail <<--------")
#         print("5 sec delay")
#         time.sleep(3)
#     #print("Output Voltage: " + str(DRQ.getVoltageOut()))
#     # print("Output Current: " + str(DRQ.getCurrent()))
#     # print("Output Power: " + str(DRQ.getPowerOut(False)) + "\n\n") #False is caclulated from given values of current and voltage while True gets values from DRQ1250

#     #DRQ.encodePMBus(34.0)

#     time.sleep(1)
