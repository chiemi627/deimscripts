#coding=utf-8

import unittest, sys,os,json,urllib2
from urllib2 import HTTPError, URLError
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
import deim

class TestDeimFunctions(unittest.TestCase):	
	def test_invalid_url_raise_exception(self):
		self.assertRaises(ValueError, lambda: deim.loadProgramInfo("",""))
		self.assertRaises(HTTPError, lambda: deim.loadProgramInfo("http://localhost/abc",""))
		self.assertRaises(ValueError, lambda: deim.loadProgramInfo("http://www.google.com",""))
		
	def test_invalid_data_raise_exception(self):
   		self.assertRaises(ValueError, lambda: deim.loadProgramInfoFromJsonData("abc",""))
   		self.assertRaises(ValueError, lambda: deim.loadProgramInfoFromJsonData("{a:bc}",""))
   		
   	def test_valid_json_data_is_parsed(self):
   		data = deim.loadProgramInfoFromJsonData("{\"value\":1}","")
   		self.assertEqual(data["value"],1)
   		data = deim.loadProgramInfoFromJsonData("var sessions = {\"value\":1}","var sessions = ")
   		self.assertEqual(data["value"],1)
   		data = deim.loadProgramInfoFromJsonData("var sessions = {\"value\":1,  }","var sessions = ")
   		self.assertEqual(data["value"],1)
   		
   	def test_session_info_canbe_detected(self):
   		program = deim.loadProgramInfoFromJsonData(u"{\"timetable\":[\"セッション1：3月6日（月） 15:20〜16:35\",\"セッション2：３月７日（火） ８：４５〜１０：１５\",]}","")
   		slots = deim.getSlotInfo(program)
   		self.assertEqual(slots["1"]["session_no"],"1")
   		self.assertEqual(slots["1"]["date"],"3/6")
   		self.assertEqual(slots["1"]["day"],1)   		
   		self.assertEqual(slots["1"]["start"],"15:20")
   		self.assertEqual(slots["1"]["end"],"16:35")
   		self.assertEqual(slots["2"]["session_no"],"2")
   		self.assertEqual(slots["2"]["date"],"3/7")
   		self.assertEqual(slots["2"]["day"],2)   		
   		self.assertEqual(slots["2"]["start"],"8:45")
   		self.assertEqual(slots["2"]["end"],"10:15")
   		
   	def test_session_info_cannotbe_detected_from_invalid_format(self):
   		program = deim.loadProgramInfoFromJsonData(u"{\"timetable\":[\"セッション1：3月6日(月) 15:20〜16:35\",\"セッション2：３月７日（火） ８：４５〜１０：１５\",]}","")
   		self.assertRaises(Exception,deim.getSlotInfo(program))
   		
	def test_invalid_url_raise_exception(self):
		self.assertRaises(ValueError, lambda: deim.getPaperInfo(""))
		self.assertRaises(HTTPError, lambda: deim.getPaperInfo("http://localhost/abc"))
		self.assertRaises(ValueError, lambda: deim.getPaperInfo("http://www.google.com"))

	def test_invalid_data_raise_exception(self):
   		self.assertRaises(ValueError, lambda: deim.getPaperInfoFromJsonData("abc"))
   		self.assertRaises(ValueError, lambda: deim.getPaperInfoFromJsonData("{a:bc}"))

   	
if __name__ == '__main__':
    unittest.main()