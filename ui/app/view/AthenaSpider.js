/*
 * File: app/view/AthenaSpider.js
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

Ext.define('spider.view.AthenaSpider', {
    extend: 'Ext.container.Viewport',

    requires: [
        'spider.view.DashboardPanel',
        'spider.view.VmManagementPanel',
        'spider.view.MyContainer1',
        'spider.view.UserManagementPanel',
        'Ext.Img',
        'Ext.toolbar.Toolbar',
        'Ext.toolbar.Fill',
        'Ext.form.Label',
        'Ext.toolbar.Separator',
        'Ext.button.Button',
        'Ext.toolbar.Spacer',
        'Ext.panel.Tool',
        'Ext.form.field.ComboBox',
        'Ext.tree.Panel',
        'Ext.tree.View',
        'Ext.tree.Column',
        'Ext.layout.container.*',
        'Ext.ux.GMapPanel',
        'Ext.util.Point',
        'Ext.data.JsonStore',
        'Ext.chart.*',
        'Ext.grid.plugin.RowEditing'
    ],

    id: 'AthenaSpider',
    itemId: 'AthenaSpider',
    layout: 'card',

    initComponent: function() {
        var me = this;

        Ext.applyIf(me, {
            items: [
                {
                    xtype: 'panel',
                    id: 'introPanel',
                    itemId: 'introPanel',
                    bodyStyle: {
                        background: 'white'
                    },
                    header: false,
                    title: 'My Panel'
                },
                {
                    xtype: 'container',
                    id: 'mainContainer',
                    width: 150,
                    layout: 'border',
                    items: [
                        {
                            xtype: 'panel',
                            margins: '0 0 5 0',
                            region: 'north',
                            height: 80,
                            id: 'northPanel',
                            itemId: 'northPanel',
                            layout: {
                                type: 'hbox',
                                align: 'stretch'
                            },
                            items: [
                                {
                                    xtype: 'panel',
                                    margins: '3 3 3 3',
                                    border: false,
                                    id: 'logoImgPanel',
                                    itemId: 'logoImgPanel',
                                    width: 197,
                                    items: [
                                        {
                                            xtype: 'image',
                                            height: 60,
                                            id: 'logoImg',
                                            itemId: 'logoImg',
                                            margin: '10 15 10 15',
                                            width: 160,
                                            src: 'resources/images/logo/osc-logo.png'
                                        }
                                    ]
                                },
                                {
                                    xtype: 'panel',
                                    flex: 1,
                                    id: 'headerPanel',
                                    itemId: 'headerPanel',
                                    layout: {
                                        type: 'vbox',
                                        align: 'stretch'
                                    },
                                    dockedItems: [
                                        {
                                            xtype: 'toolbar',
                                            flex: 1,
                                            dock: 'top',
                                            height: 30,
                                            layout: {
                                                type: 'hbox',
                                                align: 'bottom'
                                            },
                                            items: [
                                                {
                                                    xtype: 'tbfill'
                                                },
                                                {
                                                    xtype: 'label',
                                                    html: '<a href="#"><b>Administrator</b></a>',
                                                    id: 'loginUserName',
                                                    itemId: 'loginUserName',
                                                    text: 'Administrator'
                                                },
                                                {
                                                    xtype: 'tbseparator'
                                                },
                                                {
                                                    xtype: 'label',
                                                    html: '<a href="javascript:">Logout</a>',
                                                    id: 'logoutLabel',
                                                    itemId: 'logoutLabel',
                                                    margin: '0 15 0 0',
                                                    style: 'cursor: pointer;'
                                                }
                                            ]
                                        }
                                    ],
                                    items: [
                                        {
                                            xtype: 'panel',
                                            margins: '10 0 0 5',
                                            id: 'mainBtnPanel',
                                            itemId: 'mainBtnPanel',
                                            layout: {
                                                type: 'hbox',
                                                align: 'stretch'
                                            },
                                            items: [
                                                {
                                                    xtype: 'button',
                                                    height: 35,
                                                    id: 'dashboardBtn',
                                                    itemId: 'dashboardBtn',
                                                    margin: '7 0 0 0',
                                                    enableToggle: true,
                                                    icon: 'resources/images/icons/monitor.png',
                                                    pressed: true,
                                                    scale: 'medium',
                                                    text: 'Dashboard'
                                                },
                                                {
                                                    xtype: 'button',
                                                    id: 'managementBtn',
                                                    itemId: 'managementBtn',
                                                    margin: '7 0 0 0',
                                                    enableToggle: true,
                                                    icon: 'resources/images/icons/management.png',
                                                    scale: 'medium',
                                                    text: 'VM Management'
                                                },
                                                {
                                                    xtype: 'button',
                                                    id: 'monitoringBtn',
                                                    itemId: 'monitoringBtn',
                                                    margin: '7 0 0 0',
                                                    enableToggle: true,
                                                    icon: 'resources/images/icons/chart_line.png',
                                                    scale: 'medium',
                                                    text: 'Monitoring'
                                                },
                                                {
                                                    xtype: 'button',
                                                    id: 'mainViewBtn',
                                                    itemId: 'mainViewBtn',
                                                    margin: '7 0 0 0',
                                                    enableToggle: true,
                                                    icon: 'resources/images/icons/group.png',
                                                    scale: 'medium',
                                                    text: 'User Management'
                                                },
                                                {
                                                    xtype: 'label',
                                                    padding: '20 0 0 5',
                                                    width: 120,
                                                    text: 'Version : 0.05'
                                                },
                                                {
                                                    xtype: 'tbspacer',
                                                    flex: 1
                                                },
                                                {
                                                    xtype: 'label',
                                                    html: '',
                                                    itemId: 'VmHostName1',
                                                    margin: '5 0 0 0',
                                                    style: '{text-align: center;font-size : 18px;font-weight: bold;letter-spacing:10px;}',
                                                    text: '대전'
                                                },
                                                {
                                                    xtype: 'label',
                                                    html: '<center><img src="resources/images/icons/status_01.png" width="36" height="36" border="0"></center>',
                                                    itemId: 'VmHostStat1',
                                                    margin: '0 25 5 0',
                                                    minHeight: 36,
                                                    style: '{text-align: center;}',
                                                    width: 36
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            xtype: 'panel',
                            region: 'west',
                            split: true,
                            id: 'westPanel',
                            itemId: 'westPanel',
                            minWidth: 200,
                            width: 200,
                            collapsible: true,
                            title: 'Server List',
                            layout: {
                                type: 'vbox',
                                align: 'stretch'
                            },
                            tools: [
                                {
                                    xtype: 'tool',
                                    itemId: 'mytool',
                                    type: 'refresh'
                                }
                            ],
                            items: [
                                {
                                    xtype: 'panel',
                                    margins: '5 5 5 5',
                                    height: 25,
                                    id: 'locationPanel',
                                    itemId: 'locationPanel',
                                    dockedItems: [
                                        {
                                            xtype: 'combobox',
                                            dock: 'top',
                                            id: 'lnbLocationCombo',
                                            itemId: 'lnbLocationCombo',
                                            fieldLabel: 'Locations',
                                            labelWidth: 60,
                                            value: '대전',
                                            editable: false,
                                            store: [
                                                '대전',
                                                '광주'
                                            ]
                                        }
                                    ]
                                },
                                {
                                    xtype: 'panel',
                                    flex: 1,
                                    id: 'menuPanel',
                                    itemId: 'menuPanel',
                                    layout: 'border',
                                    items: [
                                        {
                                            xtype: 'panel',
                                            region: 'center',
                                            id: 'serverListPanel',
                                            itemId: 'serverListPanel',
                                            layout: {
                                                type: 'vbox',
                                                align: 'stretch'
                                            },
                                            items: [
                                                {
                                                    xtype: 'panel',
                                                    margins: '8 5 0 8',
                                                    height: 30,
                                                    id: 'btnPanel',
                                                    itemId: 'btnPanel',
                                                    layout: {
                                                        type: 'hbox',
                                                        align: 'stretch'
                                                    },
                                                    items: [
                                                        {
                                                            xtype: 'panel',
                                                            id: 'btnPanel1',
                                                            itemId: 'btnPanel1',
                                                            width: 23,
                                                            items: [
                                                                {
                                                                    xtype: 'image',
                                                                    id: 'expandImg',
                                                                    itemId: 'expandImg',
                                                                    margin: '5 0 0 0',
                                                                    style: 'cursor: pointer;',
                                                                    src: 'resources/images/icons/expand-all.png'
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            xtype: 'panel',
                                                            id: 'btnPanel2',
                                                            itemId: 'btnPanel2',
                                                            width: 15,
                                                            items: [
                                                                {
                                                                    xtype: 'image',
                                                                    margin: '5 0 0 0',
                                                                    src: 'resources/images/icons/separator.png'
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            xtype: 'panel',
                                                            id: 'btnPanel3',
                                                            itemId: 'btnPanel3',
                                                            width: 25,
                                                            items: [
                                                                {
                                                                    xtype: 'image',
                                                                    id: 'collapseImg',
                                                                    itemId: 'collapseImg',
                                                                    margin: '5 0 0 0',
                                                                    style: 'cursor: pointer;',
                                                                    src: 'resources/images/icons/collapse-all.png'
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            xtype: 'tbspacer',
                                                            flex: 0.3
                                                        },
                                                        {
                                                            xtype: 'panel',
                                                            flex: 1,
                                                            header: false,
                                                            title: 'My Panel',
                                                            items: [
                                                                {
                                                                    xtype: 'button',
                                                                    handler: function(button, e) {
                                                                        vmHostConstants.me.popAddVMHostWindow();
                                                                    },
                                                                    text: 'VM  Host 등록'
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    xtype: 'panel',
                                                    flex: 1,
                                                    id: 'listWrapPanel',
                                                    itemId: 'listWrapPanel',
                                                    layout: 'fit',
                                                    items: [
                                                        {
                                                            xtype: 'treepanel',
                                                            height: 250,
                                                            id: 'listMenuPanel',
                                                            itemId: 'listMenuPanel',
                                                            width: 400,
                                                            header: false,
                                                            title: 'My Tree Grid Panel',
                                                            hideHeaders: true,
                                                            store: 'VmHostStore',
                                                            rootVisible: false,
                                                            viewConfig: {

                                                            },
                                                            columns: [
                                                                {
                                                                    xtype: 'treecolumn',
                                                                    dataIndex: 'text',
                                                                    text: 'Nodes',
                                                                    flex: 1
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            xtype: 'container',
                            region: 'center',
                            id: 'centerContainer',
                            itemId: 'centerContainer',
                            layout: 'border',
                            items: [
                                {
                                    xtype: 'panel',
                                    region: 'center',
                                    id: 'centerPanel',
                                    itemId: 'centerPanel',
                                    layout: 'card',
                                    header: false,
                                    title: 'centerPanel',
                                    items: [
                                        {
                                            xtype: 'dashboardpanel',
                                            width: 150
                                        },
                                        {
                                            xtype: 'VmManagementPanel'
                                        },
                                        {
                                            xtype: 'mycontainer1',
                                            height: 150,
                                            id: 'samplePanel'
                                        },
                                        {
                                            xtype: 'usermanagementpanel'
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        });

        me.callParent(arguments);
    }

});