/*
 * File: app/controller/MenuController.js
 *
 * This file was generated by Sencha Architect version 3.0.4.
 * http://www.sencha.com/products/architect/
 *
 * This file requires use of the Ext JS 4.2.x library, under independent license.
 * License of Sencha Architect does not include license for Ext JS 4.2.x. For more
 * details see http://www.sencha.com/license or contact license@sencha.com.
 *
 * This file will be auto-generated each and everytime you save your project.
 *
 * Do NOT hand edit this file.
 */

Ext.define('spider.controller.MenuController', {
    extend: 'Ext.app.Controller',

    refs: [
        {
            ref: 'expandImg',
            selector: '#expandImg'
        },
        {
            ref: 'collapseImg',
            selector: '#collapseImg'
        },
        {
            ref: 'listMenuPanel',
            selector: '#listMenuPanel'
        },
        {
            ref: 'dashboardBtn',
            selector: '#dashboardBtn'
        },
        {
            ref: 'managementBtn',
            selector: '#managementBtn'
        },
        {
            ref: 'centerContainer',
            selector: '#centerContainer'
        },
        {
            ref: 'menuPanel',
            selector: '#menuPanel'
        }
    ],

    dashboardClick: function(button, e, eOpts) {
        /**
         * Dashboard 메뉴 버튼 클릭 시 수행되는 function
         */
        var centerContainer = this.getCenterContainer(),
            dashboardBtn = this.getDashboardBtn(),
            managementBtn = this.getManagementBtn(),
            menuPanel = this.getMenuPanel();

        // 현재 선택된 item이 dashboardPanel일 경우 무시한다.
        if (centerContainer.layout.getActiveItem().itemId === "dashboardPanel") {
            dashboardBtn.toggle(true);
            return;
        }

        dashboardBtn.toggle(true);
        managementBtn.toggle(false);

        Ext.getCmp('monitoringBtn').toggle(false);

        menuPanel.layout.setActiveItem(0);
        centerContainer.layout.setActiveItem(0);

        this.renderDashboard();
    },

    managementClick: function(button, e, eOpts) {
        /**
         * NFV Management 메뉴 버튼 클릭 시 수행되는 function
         */
        var centerContainer = this.getCenterContainer(),
            dashboardBtn = this.getDashboardBtn(),
            managementBtn = this.getManagementBtn(),
            menuPanel = this.getMenuPanel();

        // 현재 선택된 item이 managementPanel일 경우 무시한다.
        if (centerContainer.layout.getActiveItem().itemId === "managementPanel") {
            managementBtn.toggle(true);
            return;
        }

        managementBtn.toggle(true);
        dashboardBtn.toggle(false);

        Ext.getCmp('monitoringBtn').toggle(false);

        menuPanel.layout.setActiveItem(1);
        centerContainer.layout.setActiveItem(1);

        Ext.getCmp('hostMgmtBtn').fireEvent('click');
        Ext.getCmp('utilizationBtn').fireEvent('click');

        if (Ext.getCmp('hostGridPanel').selModel.selected.length === 0) {
            Ext.getCmp('hostGridPanel').selModel.select(0);
        }
    },

    onLaunch: function() {
        var listMenuPanel = this.getListMenuPanel();

        /**
         * Expand-All Image click event를 catch 하도록 설정
         */
        this.getExpandImg().getEl().on('click', function() {
            listMenuPanel.expandAll();
        });

        /**
         * Collapse-All Image click event를 catch 하도록 설정
         */
        this.getCollapseImg().getEl().on('click', function() {
            listMenuPanel.collapseAll();
        });

        this.renderDashboard();
    },

    renderDashboard: function() {
        var dashboardPanel = Ext.getCmp('dashboardPanel');

        dashboardPanel.setLoading(true);

        var dashboardPanels = [];
        var dashboardFieldSets = [];

        var titles = ['kh-j-nfv-host-01-ncia.go.kr','kh-j-nfv-host-02-ncia.go.kr','kh-j-nfv-host-03-ncia.go.kr','kh-j-nfv-host-04-ncia.go.kr',
                      'kh-j-nfv-host-05-ncia.go.kr','kh-j-nfv-host-06-ncia.go.kr','kh-j-nfv-host-07-ncia.go.kr','kh-j-nfv-host-08-ncia.go.kr'];
        var currentInbounds = ['23.12 kbps','12.13 kbps','8.45 kbps','3.14 kbps','54.34 kbps','5.23 kbps','2.34 kbps','1.81 kbps'];
        var averageInbounds = ['1.81 kbps','23.12 kbps','12.13 kbps','8.45 kbps','3.14 kbps','54.34 kbps','5.23 kbps','2.34 kbps'];
        var peakInbounds = ['12.13 kbps','8.45 kbps','3.14 kbps','54.34 kbps','5.23 kbps','2.34 kbps','1.81 kbps','23.12 kbps'];
        var currentOutbounds = ['12.13 kbps','8.45 kbps','3.14 kbps','54.34 kbps','5.23 kbps','2.34 kbps','1.81 kbps','23.12 kbps'];
        var averageOutbounds = ['23.12 kbps','12.13 kbps','8.45 kbps','3.14 kbps','54.34 kbps','5.23 kbps','2.34 kbps','1.81 kbps'];
        var peakOutbounds = ['1.81 kbps','23.12 kbps','12.13 kbps','8.45 kbps','3.14 kbps','54.34 kbps','5.23 kbps','2.34 kbps'];

        /*
        var serverNames = [['NFV Guest 11','NFV Guest 12','NFV Guest 13','NFV Guest 14'],
                           ['NFV Guest 21','NFV Guest 22','NFV Guest 23','NFV Guest 24'],
                           ['NFV Guest 31','NFV Guest 32','NFV Guest 33','NFV Guest 34'],
                           ['NFV Guest 41','NFV Guest 42','NFV Guest 43','NFV Guest 44'],
                           ['NFV Guest 51','NFV Guest 52','NFV Guest 53','NFV Guest 54'],
                           ['NFV Guest 61','NFV Guest 62','NFV Guest 63','NFV Guest 64'],
                           ['NFV Guest 71','NFV Guest 72','NFV Guest 73','NFV Guest 74'],
                           ['NFV Guest 81','NFV Guest 82','NFV Guest 83','NFV Guest 84']];

        var cpuStats =    [['01','02','03','04'],
                           ['05','01','02','03'],
                           ['04','05','01','02'],
                           ['03','04','05','01'],
                           ['02','03','04','05'],
                           ['01','02','03','04'],
                           ['05','01','02','03'],
                           ['04','05','01','02']];

        var memoryStats = [['03','04','05','01'],
                           ['02','03','04','05'],
                           ['01','02','03','04'],
                           ['01','02','03','04'],
                           ['05','01','02','03'],
                           ['04','05','01','02'],
                           ['05','01','02','03'],
                           ['04','05','01','02']];

        */
        /*
        var serverNames = [['NFV Guest 11','NFV Guest 12','NFV Guest 13'],
                           ['NFV Guest 21','NFV Guest 22','NFV Guest 23','NFV Guest 24'],
                           ['NFV Guest 31','NFV Guest 32','NFV Guest 33'],
                           ['NFV Guest 41','NFV Guest 42','NFV Guest 43','NFV Guest 44'],
                           ['NFV Guest 51','NFV Guest 52','NFV Guest 53'],
                           ['NFV Guest 61','NFV Guest 62','NFV Guest 63','NFV Guest 64'],
                           ['NFV Guest 71','NFV Guest 72','NFV Guest 73'],
                           ['NFV Guest 81','NFV Guest 82','NFV Guest 83','NFV Guest 84','NFV Guest 85']];

        var cpuStats =    [['01','02','03'],
                           ['05','01','02','03'],
                           ['04','05','01'],
                           ['03','04','05','01'],
                           ['02','03','04'],
                           ['01','02','03','04'],
                           ['05','01','02'],
                           ['04','05','01','02','03']];

        var memoryStats = [['03','04','05'],
                           ['02','03','04','05'],
                           ['01','02','03'],
                           ['01','02','03','04'],
                           ['05','01','02'],
                           ['04','05','01','02'],
                           ['05','01','02'],
                           ['04','05','01','02','03']];
        */

        var serverNames = [['NFV Guest 11','NFV Guest 12','NFV Guest 13','NFV Guest 14'],
                           ['NFV Guest 21','NFV Guest 22','NFV Guest 23','NFV Guest 24'],
                           ['NFV Guest 31','NFV Guest 32','NFV Guest 33','NFV Guest 34'],
                           ['NFV Guest 41','NFV Guest 42','NFV Guest 43','NFV Guest 44'],
                           ['NFV Guest 51','NFV Guest 52','NFV Guest 53','NFV Guest 54'],
                           ['NFV Guest 61','NFV Guest 62','NFV Guest 63','NFV Guest 64'],
                           ['NFV Guest 71','NFV Guest 72','NFV Guest 73','NFV Guest 74'],
                           ['NFV Guest 81','NFV Guest 82','NFV Guest 83','NFV Guest 84']];

        var cpuStats =    [['01','02','03','04'],
                           ['05','01','02','03'],
                           ['04','05','01','02'],
                           ['03','04','05','01'],
                           ['02','03','04','05'],
                           ['01','02','03','04'],
                           ['05','01','02','03'],
                           ['04','05','01','02']];

        var memoryStats = [['03','04','05','01'],
                           ['02','03','04','05'],
                           ['01','02','03','04'],
                           ['01','02','03','04'],
                           ['05','01','02','03'],
                           ['04','05','01','02'],
                           ['05','01','02','03'],
                           ['04','05','01','02']];

        for (var i = 0; i < 2; i++) {
            dashboardPanels.push(
                Ext.create('Ext.panel.Panel', {
                    requires: [
                        'Ext.form.FieldSet',
                        'Ext.panel.Panel',
                        'Ext.form.Label'
                    ],
                    layout: 'anchor',
                    columnWidth: 0.5
                })
            );
        }

        for (var i = 0; i < titles.length; i++) {
            dashboardFieldSets.push(
                Ext.create('Ext.form.FieldSet', {
                    margin: '5 5 5 5',
                    collapsible: true,
                    title: titles[i],
                    layout: {
                        type: 'hbox',
                        align: 'stretch'
                    }
                })
            );

            if (i % 2 === 0) {
                dashboardPanels[0].add(dashboardFieldSets[i]);
            } else {
                dashboardPanels[1].add(dashboardFieldSets[i]);
            }
        }

        /*
        for (var i = 0; i < titles.length; i++) {
            var panels = [];

            panels.push(
                Ext.create('Ext.panel.Panel', {
                    flex: 1,
                    layout: {
                        type: 'vbox',
                        align: 'stretch'
                    },
                    items: [
                        {
                            xtype: 'label',
                            flex: 1,
                            html: '<center><b></b></center>',
                            style: '{display:inline-block;padding-top:10px;height: 36px;}'
                        },
                        {
                            xtype: 'label',
                            flex: 1,
                            html: '<center><b></b></center>',
                            style: '{display:inline-block;padding-top:10px;height: 36px;}'
                        },
                        {
                            xtype: 'label',
                            flex: 1,
                            html: '<center><b>Current</b></center>',
                            style: '{display:inline-block;padding-top:10px;height: 36px;}'
                        },
                        {
                            xtype: 'label',
                            flex: 1,
                            html: '<center><b>Average</b></center>',
                            style: '{display:inline-block;padding-top:10px;height: 36px;}'
                        },
                        {
                            xtype: 'label',
                            flex: 1,
                            html: '<center><b>Peak</b></center>',
                            style: '{display:inline-block;padding-top:10px;height: 36px;}'
                        }
                    ]
                })
            );
            panels.push(
                Ext.create('Ext.panel.Panel', {
                    flex: 1,
                    layout: {
                        type: 'vbox',
                        align: 'stretch'
                    },
                    items: [
                        {
                            xtype: 'label',
                            flex: 1,
                            html: '<center><b></b></center>',
                            style: '{display:inline-block;padding-top:10px;height: 36px;}'
                        },
                        {
                            xtype: 'label',
                            flex: 1,
                            html: '<center><b>Inbound</b></center>',
                            style: '{display:inline-block;padding-top:10px;height: 36px;}'
                        },
                        {
                            xtype: 'label',
                            flex: 1,
                            style: '{display:inline-block;padding-top:10px;height: 36px;text-align:center;}',
                            text: currentInbounds[i]
                        },
                        {
                            xtype: 'label',
                            flex: 1,
                            style: '{display:inline-block;padding-top:10px;height: 36px;text-align:center;}',
                            text: averageInbounds[i]
                        },
                        {
                            xtype: 'label',
                            flex: 1,
                            style: '{display:inline-block;padding-top:10px;height: 36px;text-align:center;}',
                            text: peakInbounds[i]
                        }
                    ]
                })
            );
            panels.push(
                Ext.create('Ext.panel.Panel', {
                    flex: 1,
                    layout: {
                        type: 'vbox',
                        align: 'stretch'
                    },
                    items: [
                        {
                            xtype: 'label',
                            flex: 1,
                            html: '<center><b></b></center>',
                            style: '{display:inline-block;padding-top:10px;height: 36px;}'
                        },
                        {
                            xtype: 'label',
                            flex: 1,
                            html: '<center><b>Outbound</b></center>',
                            style: '{display:inline-block;padding-top:10px;height: 36px;}'
                        },
                        {
                            xtype: 'label',
                            flex: 1,
                            style: '{display:inline-block;padding-top:10px;height: 36px;text-align:center;}',
                            text: currentOutbounds[i]
                        },
                        {
                            xtype: 'label',
                            flex: 1,
                            style: '{display:inline-block;padding-top:10px;height: 36px;text-align:center;}',
                            text: averageOutbounds[i]
                        },
                        {
                            xtype: 'label',
                            flex: 1,
                            style: '{display:inline-block;padding-top:10px;height: 36px;text-align:center;}',
                            text: peakOutbounds[i]
                        }
                    ]
                })
            );
            panels.push(
                Ext.create('Ext.panel.Panel', {
                    width: 50
                })
            );
            panels.push(
                Ext.create('Ext.panel.Panel', {
                    flex: 1,
                    layout: {
                        type: 'vbox',
                        align: 'stretch'
                    },
                    items: [
                        {
                            xtype: 'label',
                            flex: 1,
                            html: '<center><b></b></center>',
                            style: '{display:inline-block;padding-top:10px;height: 36px;text-align:center;}'
                        },
                        {
                            xtype: 'label',
                            flex: 1,
                            style: '{display:inline-block;padding-top:10px;height: 36px;text-align:center;}',
                            text: serverNames[i][0]
                        },
                        {
                            xtype: 'label',
                            flex: 1,
                            style: '{display:inline-block;padding-top:10px;height: 36px;text-align:center;}',
                            text: serverNames[i][1]
                        },
                        {
                            xtype: 'label',
                            flex: 1,
                            style: '{display:inline-block;padding-top:10px;height: 36px;text-align:center;}',
                            text: serverNames[i][2]
                        },
                        {
                            xtype: 'label',
                            flex: 1,
                            style: '{display:inline-block;padding-top:10px;height: 36px;text-align:center;}',
                            text: serverNames[i][3]
                        }
                    ]
                })
            );
            panels.push(
                Ext.create('Ext.panel.Panel', {
                    flex: 1,
                    layout: {
                        type: 'vbox',
                        align: 'stretch'
                    },
                    items: [
                        {
                            xtype: 'label',
                            flex: 1,
                            html: '<center><b>CPU</b></center>',
                            style: '{display:inline-block;padding-top:10px;height: 36px;}'
                        },
                        {
                            xtype: 'label',
                            flex: 1,
                            html: '<center><img src="resources/images/icons/status_' + cpuStats[i][0] + '.png" width="36" height="36" border="0"></center>',
                            style: '{text-align: center;}'
                        },
                        {
                            xtype: 'label',
                            flex: 1,
                            html: '<center><img src="resources/images/icons/status_' + cpuStats[i][1] + '.png" width="36" height="36" border="0"></center>',
                            style: '{text-align: center;}'
                        },
                        {
                            xtype: 'label',
                            flex: 1,
                            html: '<center><img src="resources/images/icons/status_' + cpuStats[i][2] + '.png" width="36" height="36" border="0"></center>',
                            style: '{text-align: center;}'
                        },
                        {
                            xtype: 'label',
                            flex: 1,
                            html: '<center><img src="resources/images/icons/status_' + cpuStats[i][3] + '.png" width="36" height="36" border="0"></center>',
                            style: '{text-align: center;}'
                        }
                    ]
                })
            );
            panels.push(
                Ext.create('Ext.panel.Panel', {
                    flex: 1,
                    layout: {
                        type: 'vbox',
                        align: 'stretch'
                    },
                    items: [
                        {
                            xtype: 'label',
                            flex: 1,
                            html: '<center><b>Memory</b></center>',
                            style: '{display:inline-block;padding-top:10px;height: 36px;}'
                        },
                        {
                            xtype: 'label',
                            flex: 1,
                            html: '<center><img src="resources/images/icons/status_' + memoryStats[i][0] + '.png" width="36" height="36" border="0"></center>',
                            style: '{text-align: center;}'
                        },
                        {
                            xtype: 'label',
                            flex: 1,
                            html: '<center><img src="resources/images/icons/status_' + memoryStats[i][1] + '.png" width="36" height="36" border="0"></center>',
                            style: '{text-align: center;}'
                        },
                        {
                            xtype: 'label',
                            flex: 1,
                            html: '<center><img src="resources/images/icons/status_' + memoryStats[i][2] + '.png" width="36" height="36" border="0"></center>',
                            style: '{text-align: center;}'
                        },
                        {
                            xtype: 'label',
                            flex: 1,
                            html: '<center><img src="resources/images/icons/status_' + memoryStats[i][3] + '.png" width="36" height="36" border="0"></center>',
                            style: '{text-align: center;}'
                        }
                    ]
                })
            );

            dashboardFieldSets[i].add(panels);
        }
        */

        for (var i = 0; i < titles.length; i++) {
            var panels = [];

            for (var j = 0; j < 7; j++) {
                if (j === 3) {
                    panels.push(
                        Ext.create('Ext.panel.Panel', {
                            width: 50
                        })
                    );
                } else {
                    panels.push(
                        Ext.create('Ext.panel.Panel', {
                            flex: 1,
                            layout: {
                                type: 'vbox',
                                align: 'stretch'
                            }
                        })
                    );

                    if (j === 0) {
                        var diff = serverNames[i].length - 4 + 2;

                        if (diff < 1) {
                            diff = 1;
                        }

                        for (var k = 0; k < diff; k++) {
                            panels[j].add(
                                Ext.create('Ext.form.Label', {
                                    flex: 1,
                                    html: '<center><b></b></center>',
                                    style: '{display:inline-block;padding-top:10px;height: 36px;text-align:center;}'
                                })
                            );
                        }

                        panels[j].add(
                            Ext.create('Ext.form.Label', {
                                flex: 1,
                                html: '<center><b>Current</b></center>',
                                style: '{display:inline-block;padding-top:10px;height: 36px;}'
                            })
                        );
                        panels[j].add(
                            Ext.create('Ext.form.Label', {
                                flex: 1,
                                html: '<center><b>Average</b></center>',
                                style: '{display:inline-block;padding-top:10px;height: 36px;}'
                            })
                        );
                        panels[j].add(
                            Ext.create('Ext.form.Label', {
                                flex: 1,
                                html: '<center><b>Peak</b></center>',
                                style: '{display:inline-block;padding-top:10px;height: 36px;}'
                            })
                        );
                    } else if (j === 1) {
                        var diff = serverNames[i].length - 4 + 1;
                        for (var k = 0; k < diff; k++) {
                            panels[j].add(
                                Ext.create('Ext.form.Label', {
                                    flex: 1,
                                    html: '<center><b></b></center>',
                                    style: '{display:inline-block;padding-top:10px;height: 36px;text-align:center;}'
                                })
                            );
                        }

                        panels[j].add(
                            Ext.create('Ext.form.Label', {
                                flex: 1,
                                html: '<center><b>Inbound</b></center>',
                                style: '{display:inline-block;padding-top:10px;height: 36px;}'
                            })
                        );

                        panels[j].add(
                            Ext.create('Ext.form.Label', {
                                flex: 1,
                                style: '{display:inline-block;padding-top:10px;height: 36px;text-align:center;}',
                                text: currentInbounds[i]
                            })
                        );
                        panels[j].add(
                            Ext.create('Ext.form.Label', {
                                flex: 1,
                                style: '{display:inline-block;padding-top:10px;height: 36px;text-align:center;}',
                                text: averageInbounds[i]
                            })
                        );
                        panels[j].add(
                            Ext.create('Ext.form.Label', {
                                flex: 1,
                                style: '{display:inline-block;padding-top:10px;height: 36px;text-align:center;}',
                                text: peakInbounds[i]
                            })
                        );
                    } else if (j === 2) {
                        var diff = serverNames[i].length - 4 + 1;
                        for (var k = 0; k < diff; k++) {
                            panels[j].add(
                                Ext.create('Ext.form.Label', {
                                    flex: 1,
                                    html: '<center><b></b></center>',
                                    style: '{display:inline-block;padding-top:10px;height: 36px;text-align:center;}'
                                })
                            );
                        }

                        panels[j].add(
                            Ext.create('Ext.form.Label', {
                                flex: 1,
                                html: '<center><b>Outbound</b></center>',
                                style: '{display:inline-block;padding-top:10px;height: 36px;}'
                            })
                        );

                        panels[j].add(
                            Ext.create('Ext.form.Label', {
                                flex: 1,
                                style: '{display:inline-block;padding-top:10px;height: 36px;text-align:center;}',
                                text: currentOutbounds[i]
                            })
                        );
                        panels[j].add(
                            Ext.create('Ext.form.Label', {
                                flex: 1,
                                style: '{display:inline-block;padding-top:10px;height: 36px;text-align:center;}',
                                text: averageOutbounds[i]
                            })
                        );
                        panels[j].add(
                            Ext.create('Ext.form.Label', {
                                flex: 1,
                                style: '{display:inline-block;padding-top:10px;height: 36px;text-align:center;}',
                                text: peakOutbounds[i]
                            })
                        );
                    } else if (j === 4) {
                        panels[j].add(
                            Ext.create('Ext.form.Label', {
                                flex: 1,
                                html: '<center><b></b></center>',
                                style: '{display:inline-block;padding-top:10px;height: 36px;text-align:center;}'
                            })
                        );
                    } else if (j === 5) {
                        panels[j].add(
                            Ext.create('Ext.form.Label', {
                                flex: 1,
                                html: '<center><b>CPU</b></center>',
                                style: '{display:inline-block;padding-top:10px;height: 36px;text-align:center;}'
                            })
                        );
                    } else if (j === 6) {
                        panels[j].add(
                            Ext.create('Ext.form.Label', {
                                flex: 1,
                                html: '<center><b>Memory</b></center>',
                                style: '{display:inline-block;padding-top:10px;height: 36px;text-align:center;}'
                            })
                        );
                    }
                }
            }

            var len = serverNames[i].length;
            for (var k = 0; k < len; k++) {
                panels[4].add(
                    Ext.create('Ext.form.Label', {
                        flex: 1,
                        style: '{display:inline-block;padding-top:10px;height: 36px;text-align:center;}',
                        text: serverNames[i][k]
                    })
                );

                panels[5].add(
                    Ext.create('Ext.form.Label', {
                        flex: 1,
                        html: '<center><img src="resources/images/icons/status_' + cpuStats[i][k] + '.png" width="36" height="36" border="0"></center>',
                        style: '{text-align: center;}'
                    })
                );

                panels[6].add(
                    Ext.create('Ext.form.Label', {
                        flex: 1,
                        html: '<center><img src="resources/images/icons/status_' + memoryStats[i][k] + '.png" width="36" height="36" border="0"></center>',
                        style: '{text-align: center;}'
                    })
                );
            }

            dashboardFieldSets[i].add(panels);
        }

        dashboardPanel.removeAll();
        dashboardPanel.add(dashboardPanels);

        dashboardPanel.setLoading(false);
    },

    init: function(application) {
        this.control({
            "#dashboardBtn": {
                click: this.dashboardClick
            },
            "#managementBtn": {
                click: this.managementClick
            }
        });
    }

});
