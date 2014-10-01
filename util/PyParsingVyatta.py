# jsonParser.py
#
# Implementation of a simple JSON parser, returning a hierarchical
# ParseResults object support both list- and dict-style data access.
#
# Copyright 2006, by Paul McGuire
#
# Updated 8 Jan 2007 - fixed dict grouping bug, and made elements and
#   members optional in array and object collections
#

import json

vyatta_bnf = """
config =
	{ rootKeywords* }
rootKeywords
	{ elementList }
elementList
	itemOrElement*
element 
    string [string] { itemOrElement* }
itemOrElement
	{item|element|unaryItem}
item
    string value EndOfLine
unaryItem
	string EndOfLine
value 
    word
    number
"""

from pyparsing import *

keywords = CaselessKeyword('interfaces') | CaselessKeyword('nat') | CaselessKeyword('service') | CaselessKeyword('system')
elementList = Forward()
string = Word( alphanums+'_-:/.+@$' )
number = Combine( Optional('-') + ( '0' | Word('123456789',nums) ) +
                   Optional( '.' + Word(nums) ) +
                   Optional( Word('eE',exact=1) + Word(nums+'+-',nums) ) )
value = string | number | dblQuotedString.setParseAction(removeQuotes)
unaryItem = Group(value + Suppress(lineEnd()))
item = Group(string + value + Suppress(lineEnd()))
element = Forward()
itemOrElement = item | unaryItem | element
element << Group(string + Optional(string) + Group(Suppress('{') + ZeroOrMore(itemOrElement) + Suppress('}')))
elementList = ZeroOrMore(itemOrElement)
rootKeywords = keywords + Group( Suppress('{') + elementList + Suppress('}'))
config = OneOrMore(rootKeywords)
vbash_message = Regex(r"vbash\:.*").setName("vbash message")
config.ignore(vbash_message)

def convertNumbers(s,l,toks):
    n = toks[0]
    try:
        return int(n)
    except ValueError, ve:
        return float(n)
        
number.setParseAction( convertNumbers )
    
if __name__ == "__main__":
	testdata = """
	service {
	    dhcp-server {
	        disabled false
	        shared-network-name MYLAN1 {
	            authoritative disable
	            subnet 192.168.99.0/24 {
	                default-router 192.168.99.1
	                dns-server 192.168.99.1
	                domain-name vyatta.local
	                lease 86400
	                start 192.168.99.101 {
	                    stop 192.168.99.200
	                }
	            }
	        }
	    }
	    dns {
	        forwarding {
	            cache-size 150
	            listen-on eth1
	            name-server 8.8.8.8
	        }
	    }
	    https {
	        http-redirect enable
	    }
	    ssh {
	        allow-root
	        port 22
	    }
	}
	"""
	
	testdata2 = """
	interfaces {
	    ethernet eth0 {
	        address dhcp
	        duplex auto
	        hw-id 08:00:27:78:42:c3
	        smp_affinity auto
	        speed auto
	    }
	    ethernet eth1 {
	        address 192.168.99.1/24
	        duplex auto
	        hw-id 08:00:27:89:09:16
	        smp_affinity auto
	        speed auto
	    }
	    ethernet eth2 {
	        address 192.168.56.13/24
	        duplex auto
	        hw-id 08:00:27:35:47:6a
	        smp_affinity auto
	        speed auto
	    }
	    loopback lo {
	    }
	}
	nat {
	    source {
	        rule 10 {
	            outbound-interface eth0
	            source {
	                address 192.168.99.1/24
	            }
	            translation {
	                address masquerade
	            }
	        }
	    }
	}
	service {
	    dhcp-server {
	        disabled false
	        shared-network-name MYLAN1 {
	            authoritative disable
	            subnet 192.168.99.0/24 {
	                default-router 192.168.99.1
	                dns-server 192.168.99.1
	                domain-name vyatta.local
	                lease 86400
	                start 192.168.99.101 {
	                    stop 192.168.99.200
	                }
	            }
	        }
	    }
	    dns {
	        forwarding {
	            cache-size 150
	            listen-on eth1
	            name-server 8.8.8.8
	        }
	    }
	    https {
	        http-redirect enable
	    }
	    ssh {
	        allow-root
	        port 22
	    }
	}
	system {
	            components "ab c"
	    config-management {
	        commit-revisions 20
	    }
	    console {
	        device ttyS0 {
	            speed 9600
	        }
	    }
	    host-name vyatta
	    login {
	        user vyatta {
	            authentication {
	                encrypted-password $1$NdMWfsCo$GnzdIoHV74BM.lRQA1ROu0
	                public-keys vyatta@vyatta {
	                    key AAAAB3NzaC1yc2EAAAADAQABAAABAQC19QkW/1mWrBBvy8VmntJXxXYGGqgEFVeBy+BTjkTCt9Mq8MQPbLl2rPITc/fn20hO5Ttg3oC9vdvQ1MKCstHr8DuBswFOsv21nV7+DlB+6NzSkS8FyAQs5hCtGdYSsBHqCd7QWkB/rCfpQ3W1xx+whqnw/Z+GPyeBRmLeuRHUkmzRdB0arhorab4P+aLTGTrtA0AA2/216n4WliXC5PFrTiqfSmscYGPtpMAfrK0/cLIP3LPDDK0rNFUaWGP3gNWwxyPrJzoNKuXlJxsW9DMQyUpKhjlaTDGB26Y86LVKB1mUOdINh5V0izGqWx8Do54GRpsVxtRsIM3F90pQN0Pn
	                    type ssh-rsa
	                }
	            }
	            level admin
	        }
	    }
	    ntp {
	        server 0.vyatta.pool.ntp.org {
	        }
	        server 1.vyatta.pool.ntp.org {
	        }
	        server 2.vyatta.pool.ntp.org {
	        }
	    }
	    package {
	        auto-sync 1
	        repository community {
	            components main
	            distribution stable
	            password ""
	            url http://packages.vyatta.com/vyatta
	            username ""
	        }
	        repository squeeze {
	            components "main contrib non-free"
	            distribution squeeze
	            password ""
	            url http://mirrors.kernel.org/debian
	            username ""
	        }
	    }
	    syslog {
	        global {
	            facility all {
	                level notice
	            }
	            facility protocols {
	                level debug
	            }
	        }
	    }
	    time-zone GMT
	}
	"""

	import pprint
	results = elementList.parseString(testdata)
 	pprint.pprint( results.asList() )

	services =[]
	for svc in results.asList():
		print svc
		service = {'service': svc[0]}
		
		for attr in svc[1]:
			if len(attr) > 1:
				service[attr[0]] = attr[1]
			else:
				service[attr[0]] = True
		
		services.append(service)

	print json.dumps(services, indent=4)

