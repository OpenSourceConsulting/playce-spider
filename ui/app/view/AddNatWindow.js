/*
 * File: app/view/AddNatWindow.js
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

Ext.define('spider.view.AddNatWindow', {
    extend: 'Ext.window.Window',
    alias: 'widget.AddNatWindow',

    requires: [
        'Ext.form.Panel',
        'Ext.form.RadioGroup',
        'Ext.form.field.Radio',
        'Ext.form.field.ComboBox',
        'Ext.toolbar.Spacer',
        'Ext.toolbar.Toolbar',
        'Ext.button.Button'
    ],

    height: 375,
    id: 'AddBondingWindow1',
    width: 700,
    resizable: false,
    title: 'NAT 등록',
    modal: true,

    initComponent: function() {
        var me = this;

        Ext.applyIf(me, {
            items: [
                {
                    xtype: 'form',
                    id: 'addNatForm',
                    bodyPadding: 10,
                    header: false,
                    title: 'My Form',
                    fieldDefaults: {
                        msgTarget: 'side',
                        labelStyle: 'color:#666;font-weight: bold;text-align: right;',
                        labelSeparator: ' : ',
                        margin: '0 10 0 0',
                        labelWidth: 145
                    },
                    items: [
                        {
                            xtype: 'fieldcontainer',
                            flex: '1',
                            height: 35,
                            fieldLabel: 'Label',
                            hideLabel: true,
                            layout: {
                                type: 'hbox',
                                align: 'middle'
                            },
                            items: [
                                {
                                    xtype: 'textfield',
                                    flex: 1,
                                    fieldLabel: 'Rule Num',
                                    name: 'rulenum',
                                    allowBlank: false
                                },
                                {
                                    xtype: 'radiogroup',
                                    flex: 1,
                                    width: 300,
                                    fieldLabel: 'Rule Type',
                                    allowBlank: false,
                                    items: [
                                        {
                                            xtype: 'radiofield',
                                            width: 70,
                                            name: 'ruletype',
                                            boxLabel: 'Source',
                                            inputValue: 'source'
                                        },
                                        {
                                            xtype: 'radiofield',
                                            width: 100,
                                            name: 'ruletype',
                                            boxLabel: 'Destination',
                                            inputValue: 'destination'
                                        }
                                    ],
                                    listeners: {
                                        change: {
                                            fn: me.onRadiogroupChange,
                                            scope: me
                                        }
                                    }
                                }
                            ]
                        },
                        {
                            xtype: 'fieldcontainer',
                            flex: '1',
                            height: 35,
                            fieldLabel: 'Label',
                            hideLabel: true,
                            layout: {
                                type: 'hbox',
                                align: 'middle'
                            },
                            items: [
                                {
                                    xtype: 'combobox',
                                    flex: 1,
                                    fieldLabel: 'Inbound Interface',
                                    name: 'ibnic',
                                    allowBlank: false,
                                    editable: false,
                                    displayField: 'ethName',
                                    queryMode: 'local',
                                    valueField: 'ethName'
                                },
                                {
                                    xtype: 'combobox',
                                    flex: 1,
                                    fieldLabel: 'Outbound Interface',
                                    name: 'obnic',
                                    allowBlank: false,
                                    editable: false,
                                    displayField: 'ethName',
                                    queryMode: 'local',
                                    valueField: 'ethName'
                                }
                            ]
                        },
                        {
                            xtype: 'fieldcontainer',
                            flex: '1',
                            height: 35,
                            fieldLabel: 'Label',
                            hideLabel: true,
                            layout: {
                                type: 'hbox',
                                align: 'middle'
                            },
                            items: [
                                {
                                    xtype: 'textfield',
                                    flex: 1,
                                    fieldLabel: 'Source Address',
                                    name: 'srcaddr'
                                },
                                {
                                    xtype: 'textfield',
                                    flex: 1,
                                    fieldLabel: 'Destination Address',
                                    name: 'destaddr'
                                }
                            ]
                        },
                        {
                            xtype: 'fieldcontainer',
                            flex: '1',
                            height: 35,
                            fieldLabel: 'Label',
                            hideLabel: true,
                            layout: {
                                type: 'hbox',
                                align: 'middle'
                            },
                            items: [
                                {
                                    xtype: 'textfield',
                                    flex: 1,
                                    fieldLabel: 'Source Port',
                                    name: 'srcport'
                                },
                                {
                                    xtype: 'textfield',
                                    flex: 1,
                                    fieldLabel: 'Destination Port',
                                    name: 'destport'
                                }
                            ]
                        },
                        {
                            xtype: 'fieldcontainer',
                            flex: '1',
                            height: 35,
                            fieldLabel: 'Label',
                            hideLabel: true,
                            layout: {
                                type: 'hbox',
                                align: 'middle'
                            },
                            items: [
                                {
                                    xtype: 'textfield',
                                    flex: 1,
                                    margin: '0 20 0 0',
                                    fieldLabel: 'Protocol',
                                    name: 'protocol'
                                },
                                {
                                    xtype: 'tbspacer',
                                    flex: 1
                                }
                            ]
                        },
                        {
                            xtype: 'fieldcontainer',
                            flex: '1',
                            height: 35,
                            fieldLabel: 'Label',
                            hideLabel: true,
                            layout: {
                                type: 'hbox',
                                align: 'middle'
                            },
                            items: [
                                {
                                    xtype: 'textfield',
                                    flex: 1,
                                    fieldLabel: 'Translation Address',
                                    name: 'transaddr',
                                    allowBlank: false
                                },
                                {
                                    xtype: 'checkboxfield',
                                    flex: 1,
                                    fieldLabel: '',
                                    name: 'masquerade',
                                    boxLabel: 'Masquerade',
                                    listeners: {
                                        change: {
                                            fn: me.onCheckboxfieldChange,
                                            scope: me
                                        }
                                    }
                                }
                            ]
                        },
                        {
                            xtype: 'fieldcontainer',
                            flex: '1',
                            height: 35,
                            fieldLabel: 'Label',
                            hideLabel: true,
                            layout: {
                                type: 'hbox',
                                align: 'middle'
                            },
                            items: [
                                {
                                    xtype: 'textfield',
                                    flex: 1,
                                    margin: '0 20 0 0',
                                    fieldLabel: 'Translation Port',
                                    name: 'transport'
                                },
                                {
                                    xtype: 'tbspacer',
                                    flex: 1
                                }
                            ]
                        },
                        {
                            xtype: 'fieldcontainer',
                            flex: '1',
                            height: 35,
                            fieldLabel: 'Label',
                            hideLabel: true,
                            layout: {
                                type: 'hbox',
                                align: 'middle'
                            },
                            items: [
                                {
                                    xtype: 'checkboxgroup',
                                    flex: 1,
                                    width: 400,
                                    fieldLabel: 'Options',
                                    items: [
                                        {
                                            xtype: 'checkboxfield',
                                            name: 'disable',
                                            boxLabel: 'Disable'
                                        },
                                        {
                                            xtype: 'checkboxfield',
                                            name: 'exclude',
                                            boxLabel: 'Exclude'
                                        }
                                    ]
                                },
                                {
                                    xtype: 'tbspacer',
                                    flex: 1
                                }
                            ]
                        }
                    ],
                    dockedItems: [
                        {
                            xtype: 'toolbar',
                            dock: 'bottom',
                            ui: 'footer',
                            layout: {
                                type: 'hbox',
                                pack: 'center'
                            },
                            items: [
                                {
                                    xtype: 'button',
                                    handler: function(button, e) {
                                        vmConstants.me.createVMNat(button);
                                    },
                                    padding: '3 8 3 8',
                                    text: '저장'
                                },
                                {
                                    xtype: 'button',
                                    handler: function(button, e) {
                                        GLOBAL.me.closeWindow(button);
                                    },
                                    padding: '3 8 3 8',
                                    text: '취소'
                                }
                            ]
                        }
                    ],
                    listeners: {
                        render: {
                            fn: me.onAddNatFormRender,
                            scope: me
                        }
                    }
                }
            ]
        });

        me.callParent(arguments);
    },

    onRadiogroupChange: function(field, newValue, oldValue, eOpts) {
        var form = field.up('form');

        if(newValue.ruletype == 'source') {
            form.getForm().findField("ibnic").setDisabled(true);
            form.getForm().findField("obnic").setDisabled(false);
        } else {
            form.getForm().findField("ibnic").setDisabled(false);
            form.getForm().findField("obnic").setDisabled(true);
        }

    },

    onCheckboxfieldChange: function(field, newValue, oldValue, eOpts) {
        var form = field.up('form').getForm();
        if(newValue == true) {
            form.findField("transaddr").setValue("");
            form.findField("transport").setValue("");

            form.findField("transaddr").setDisabled(true);
            form.findField("transport").setDisabled(true);
        } else {
            form.findField("transaddr").setDisabled(false);
            form.findField("transport").setDisabled(false);
        }
    },

    onAddNatFormRender: function(component, eOpts) {
        var components = [component.getForm().findField("ibnic"), component.getForm().findField("obnic")];

        vmConstants.me.renderNicComboBox(components, component.getEl());
    }

});