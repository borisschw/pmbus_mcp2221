import time, logging
from pmbus import PMBus


# Import preset mappings

class RPB_Charger:
    def __init__(self):
        # print("RPB Charger init")
        self.RPB = PMBus(0x47,1) #New pmbus object with device address 0x47
        print("PM Bus Version = {} ".format(self.RPB.getPmbusRev()))
        print("--->> RPB Charger init")
        print("Exponent = {} ".format(self.RPB.getExponent()))



    def config_curve(self, val):
        return self.config_param(self.RPB.setCurveConfig, self.RPB.getCurveConfig, val)

    def config_ichg(self, val):
        return self.config_param(self.RPB.setCurve_ICHG, self.RPB.getCurve_ICHG, val)

    def config_vbst(self, val):
        return self.config_param(self.RPB.setCurve_vbst, self.RPB.getCurve_vbst, val)

    def config_vfloat(self, val):
        return self.config_param(self.RPB.setCurve_vfloat, self.RPB.getCurve_vfloat, val)

    def config_cc_timeout(self, val):
        return self.config_param(self.RPB.set_ccTimeout, self.RPB.get_ccTimeout, val)

    def config_cv_timeout(self, val):
        return self.config_param(self.RPB.set_cvTimeout, self.RPB.get_cvTimeout, val)

    def config_float_timeout(self, val):
        return self.config_param(self.RPB.set_floatTimeout, self.RPB.get_floatTimeout, val)

    def config_iout(self, val):
        return self.config_param(self.RPB.setIoutOCLimit, self.RPB.getIoutOCLimit, val)

    def config_vout_trim(self, val):
        return self.config_param(self.RPB.setVoutTrim, self.RPB.getVoutTrim, val)


    def config_param(self, setter,getter,val):
        time.sleep(2)
        setter(val)
        time.sleep(2)
        ret_val = getter()
        print("send val = {}, ret val = {}".format(val, ret_val) )

        if (ret_val == val):
            return True
        return False


    def get_status(self):
        ret = {}

        try:
            print("getStatusSummary")
            status, reg_val = self.RPB.getStatusSummary()

            ret['busy'] = status['busy']
            ret['off'] = status['off']
            ret['vout_ov_fault'] = status['vout_ov_fault']
            ret['iout_oc_fault'] = status['iout_oc_fault']
            ret['vin_uv_fault'] = status['vin_uv_fault']
            ret['temp_fault'] = status['temp_fault']
            ret['cml_fault'] = status['cml_fault']
            ret['vout_fault'] = status['vout_fault']
            ret['iout_fault'] = status['iout_fault']
            ret['input_fault'] = status['input_fault']
            ret['pwr_gd'] = status['pwr_gd']
            ret['fan_fault'] = status['fan_fault']

            ("getVoltageOut")
            ret['vout'] = self.RPB.getVoltageOut()
            time.sleep(1)

            print("getVoltageIn")
            ret['vin']  = self.RPB.getVoltageIn()
            time.sleep(1)

            print("getCurrent")
            ret['iout']  = self.RPB.getCurrent()
            time.sleep(1)

            ret['mode'] = "charging" if (ret['vout'] > 18 and ret['off'] == False) else "monitoring"
            time.sleep(1)
            self.last_status = ret
        except Exception as e:
            print("RPB Charger failed to get new data: " + str(e))



    def rpbConfigure(self):

        set_vout_ok = False
        set_iout_ok = False
        iout_limit = 20
        vout_limit = 28


        print("----------->>>Initial settings iout = {}, vout = {}".format(iout_limit,vout_limit ))

        try:
            if (iout_limit < 55 and iout_limit >= 0):
                if (self.config_iout(iout_limit)):
                    print("config_iout was sccessful")
                    set_iout_ok = True
                else:
                    print("--->>>Failed to set config_iout <<<--- ")
                    self.turn_off(hard=True)
            else:
                print("The iout limit is not correct")
                return -1

            if(vout_limit >= 18 and vout_limit <= 30):
                if (self.config_vout_trim(vout_limit - 24)):
                    set_vout_ok = True
                    print("config_vout_trim was sccessful")
                else:
                    print("--->>>Failed to set config_vout_trim <<<--- ")
                    self.turn_off(hard=True)
            else:
                print("The vout limit is not correct")
                return -1

            if (set_vout_ok and set_iout_ok):
                print("Sccessful Config - turn on the charger")
                self.RPB.regOn()
                return True
            else:
                return False
        except Exception as e:
            print("--->>>Failed to set config RPB charger <<<--- "+ str(e))
            self.turn_off(hard=True)
            return False


    def turn_off(self, hard=False):
        try:
            self.RPB.regOff(hard)
        except Exception as e:
            print("RPB Charger failed turn off"+ str(e))


        # iout = 0
        # vout_trim = 0
        # # print(self.RPB.getStatusSummary())
        # # print("FW version = ", "".join([chr(x) for x in self.RPB.getMfrRevision()]))
        # # print("OC Response",hex(self.RPB.getIoutFaultResponse()))
        # print("Vout = ", self.RPB.getVoltageOut())
        # time.sleep(1)
        # print("Vin = ",self.RPB.getVoltageIn())
        # time.sleep(1)
        # iout = self.RPB.getCurrent()
        # print("Iout = ",iout)
        # time.sleep(1)
        # # if (iout < 15.0):
        # #     vout_trim = self.RPB.getVoutTrim()
        # #     time.sleep(1)
        # #     config_vout_trim(int(vout_trim) + 1)
        # #     print("new vout trim = ", vout_trim +1 )
        # print("")

        # time.sleep(3)
