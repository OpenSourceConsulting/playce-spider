#-*- coding: utf-8 -*-
# ########################## Copyrights and license ############################################
#                                                                                              #
# Copyright 2014 Open Source Consulting, Inc. <support@osci.kr>                                #
#                                                                                              #
# This file is part of athena-spider. https://github.com/OpenSourceConsulting/athena-spider    #
#                                                                                              #
# athena-spider is free software: you can redistribute it and/or modify it under               #
# the terms of the GNU Lesser General Public License as published by the Free                  #
# Software Foundation, either version 3 of the License, or (at your option)                    #
# any later version.                                                                           #
#                                                                                              #
# athena-spider is distributed in the hope that it will be useful, but WITHOUT ANY             #
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS                    #
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more                 #
# details.                                                                                     #
#                                                                                              #
# You should have received a copy of the GNU Lesser General Public License                     #
# along with athena-spider. If not, see <http://www.gnu.org/licenses/>.                        #
#                                                                                              #
# ##############################################################################################
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