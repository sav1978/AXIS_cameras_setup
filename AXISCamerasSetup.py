#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from lxml import etree as et
import unittest, time


class AXISCamSetup(unittest.TestCase):
    def setUp(self):
        print "Hello!"
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        print "Firefox started!"
        self.cams = []
        self.tree = et.parse("cameras.xml")
        cameras = self.tree.xpath("/cameras/cam[@configured='0']")
        for camera in cameras:
            self.cams.append({"ipAddress":camera.get("ipAddress"),
                              "model":camera.get("model"),
                              "macAddress":camera.get("macAddress")})
        self.base_url = "http://root:9600613@"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def setupAXISCamera(self, camera):
        driver = self.driver
        driver.get(self.base_url + camera["ipAddress"] + "/operator/videostream.shtml?id=0")
        cam_model = driver.find_element_by_id("tincl_prodName").text.split()[1]
        self.assertEqual(camera["model"], cam_model)
        print "Seting up camera " + camera["model"] + "( ip: " + camera["ipAddress"] + " )"
        if cam_model == "P1354" or cam_model == "P1365" or cam_model == "P3304":
            Select(driver.find_element_by_id("idResolution")).select_by_visible_text("1280x800 (16:10)")
        elif cam_model == "P3224-LV" or cam_model == "P3224-LVE" or cam_model == "Q6044-E" or cam_model == "Q6114-E":
            Select(driver.find_element_by_id("idResolution")).select_by_visible_text("1280x720 (16:9)")
        driver.find_element_by_name("root_Image_I0_Appearance_Compression").clear()
        driver.find_element_by_name("root_Image_I0_Appearance_Compression").send_keys("30")
        if cam_model == "P1354" or cam_model == "P3304":
            driver.find_element_by_xpath("//*[@id='image']/table/tbody/tr[9]/td/input[1]").click()
        elif cam_model == "P1365" or cam_model == "P3224-LV" or cam_model == "P3224-LVE":
            driver.find_element_by_xpath("//*[@id='image']/table/tbody/tr[10]/td/input[1]").click()
        elif cam_model == "Q6044-E" or cam_model == "Q6114-E":
            driver.find_element_by_xpath("//*[@id='image']/table/tbody/tr[8]/td/input[1]").click()
        driver.find_element_by_name("Image_I0_Stream_FPS").clear()
        driver.find_element_by_name("Image_I0_Stream_FPS").send_keys("15")
        if cam_model == "P1354" or cam_model == "P3304":
            driver.find_element_by_id("strDef_SaveBtn").click()
        else:
            driver.find_element_by_id("vidStrm_SaveBtn").click()
        driver.get(self.base_url + camera["ipAddress"] + "/operator/streamprofilelist.shtml?id=0")
        if cam_model == "P1354" or cam_model == "P3304":
            profiles_opt = driver.find_elements_by_xpath("//select[@name='ProfileList']/option")
            for profile in profiles_opt:
                if profile.text.lower().startswith("quality"):
                    profile.click()
                    break
        else:
            driver.find_element_by_xpath("//*[@id='idListContainer']/table/tbody/tr[@title='Quality']").click()
        main_window_handle = None
        while not main_window_handle:
            main_window_handle = driver.current_window_handle
        driver.find_element_by_xpath("//input[@value='Modify...']").click()
        time.sleep(3)
        signin_window_handle = None
        while not signin_window_handle:
            for handle in driver.window_handles:
                if handle != main_window_handle:
                    signin_window_handle = handle
                    break
        driver.switch_to.window(signin_window_handle)
        driver.switch_to.frame(driver.find_element_by_name("settings"))
        if cam_model == "P1354" or cam_model == "P1365":
            Select(driver.find_element_by_id("resolution")).select_by_visible_text("1280x800")
        elif cam_model == "P3224-LV" or cam_model == "P3224-LVE" or cam_model == "Q6044-E" or cam_model == "Q6114-E":
            Select(driver.find_element_by_id("resolution")).select_by_visible_text("1280x720")
        elif cam_model == "P3304":
            Select(driver.find_element_by_name("resolution")).select_by_visible_text("1280x800 (16:10)")
        driver.find_element_by_name("compression").clear()
        driver.find_element_by_name("compression").send_keys("35")
        driver.find_element_by_xpath("//*[@id='fpsConf']/table/tbody/tr[2]/td/input[@value='limited']").click()
        driver.find_element_by_name("fps").clear()
        driver.find_element_by_name("fps").send_keys("15")
        driver.find_element_by_name("save").click()
        driver.switch_to.window(main_window_handle)
        if cam_model == "P1354" or cam_model == "P3304":
            profiles_opt = driver.find_elements_by_xpath("//select[@name='ProfileList']/option")
            for profile in profiles_opt:
                if profile.text.lower().startswith("mobile"):
                    profile.click()
                    break
        else:
            driver.find_element_by_xpath("//*[@id='idListContainer']/table/tbody/tr[@title='Mobile']").click()
        main_window_handle = None
        while not main_window_handle:
            main_window_handle = driver.current_window_handle
        driver.find_element_by_xpath("//input[@value='Modify...']").click()
        time.sleep(3)
        signin_window_handle = None
        while not signin_window_handle:
            for handle in driver.window_handles:
                if handle != main_window_handle:
                    signin_window_handle = handle
                    break
        driver.switch_to.window(signin_window_handle)
        driver.switch_to.frame(driver.find_element_by_name("settings"))
        if cam_model == "P1354" or cam_model == "P1365" or cam_model == "P3224-LV" or cam_model == "P3224-LVE":
            Select(driver.find_element_by_id("resolution")).select_by_visible_text("480x360")
        elif cam_model == "Q6044-E" or cam_model == "Q6114-E":
            Select(driver.find_element_by_id("resolution")).select_by_visible_text("480x270")
        elif cam_model == "P3304":
            Select(driver.find_element_by_name("resolution")).select_by_visible_text("480x360 (4:3)")
        driver.find_element_by_name("save").click()
        driver.switch_to.window(main_window_handle)
        time.sleep(5)
        if cam_model == "P1354" or cam_model == "P1365" or cam_model == "P3224-LV" or cam_model == "P3224-LVE" or cam_model == "P3304":
            print "Need to advanced settings of anti-flicker defense ... "
            driver.get(self.base_url + camera["ipAddress"] + "/operator/advanced.shtml?nbr=0&id=0")
            if cam_model == "P1354" or cam_model == "P3304":
                Select(driver.find_element_by_name("root_ImageSource_I0_Sensor_Exposure")).select_by_visible_text("Flicker-free 50 Hz")
            else:
                Select(driver.find_element_by_name("root_ImageSource_I0_Sensor_Exposure")).select_by_visible_text(
                    "Flicker-reduced 50 Hz")
            time.sleep(15)
            driver.find_element_by_id("adv_SaveBtn").click()
        cam = self.tree.xpath("/cameras/cam[@ipAddress='" + camera["ipAddress"] + "']")
        for item in cam:
            item.attrib["configured"] = "1"

    def test_AXISCams(self):
        for cam in self.cams:
            self.setupAXISCamera(cam)
            f = open("cameras.xml", "w")
            f.write(et.tostring(self.tree, pretty_print=True, xml_declaration=True, encoding='utf-8'))
            f.close()

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
