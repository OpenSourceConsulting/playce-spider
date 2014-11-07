#-*- coding: utf-8 -*-
'''---------------------------------
	파이썬 공통 유틸함수들.
	
	Created on 2014. 11. 7.
	@author: Bong-Jin Kwon
---------------------------------'''
from spidercore import *

logger = logging.getLogger(__name__)


""" vyatta 설정 변경사항만 가져오기
	- orgin_dic 와 new_dic 이 동일한 항목을 유지한다고 전제함.
	
	@param orgin_dic:   original dictionary to diff.
	@param new_dic:  new dicationary to diff.
	@return diff:   변경된 설정 항목만 포함된 dicationary
"""
def diff_vyatta_conf(orgin_dic, new_dic):
	
	diff = {}
	
	for key in orgin_dic.keys():
		if (orgin_dic[key] != new_dic[key]):
			diff[key] = new_dic[key]
	return diff