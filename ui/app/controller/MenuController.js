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
            ref: 'monitoringBtn',
            selector: '#monitoringBtn'
        },
        {
            ref: 'userManagementBtn',
            selector: '#userManagementBtn'
        },
        {
            ref: 'centerContainer',
            selector: '#centerPanel'
        },
        {
            ref: 'mytool',
            selector: '#mytool'
        },
        {
            ref: 'menuPanel',
            selector: '#menuPanel'
        }
    ],

    dashboardClick: function(button, e, eOpts) {
        this.toggleDashboardBtn();

        // 현재 선택된 item이 dashboardPanel일 경우 무시한다.

        var centerContainer = this.getCenterContainer();
        if (centerContainer.layout.getActiveItem().itemId === "DashboardPanel") {
            return;
        }

        dashboardConstants.me.renderDashboard();

    },

    managementClick: function(button, e, eOpts) {
        /**
         * NFV Management 메뉴 버튼 클릭 시 수행되는 function
         */
        this.viewManagementMenu();
    },

    onMonitoringBtnClick: function(button, e, eOpts) {

        /**
         * Sample 메뉴 버튼 클릭 시 수행되는 function
         */
        var centerContainer = this.getCenterContainer(),
            dashboardBtn = this.getDashboardBtn(),
            managementBtn = this.getManagementBtn(),
            monitoringBtn = this.getMonitoringBtn(),
            userManagementBtn = this.getUserManagementBtn(),
            menuPanel = this.getMenuPanel();

        dashboardBtn.toggle(false);
        managementBtn.toggle(false);
        userManagementBtn.toggle(false);
        monitoringBtn.toggle(true);

        centerContainer.layout.setActiveItem(2);

        monitoringConstants.me.initMonitoring();
    },

    onUserManagementBtnBtnClick: function(button, e, eOpts) {

        /**
         * Main View 메뉴 버튼 클릭 시 수행되는 function
         */
        var centerContainer = this.getCenterContainer(),
            dashboardBtn = this.getDashboardBtn(),
            managementBtn = this.getManagementBtn(),
            monitoringBtn = this.getMonitoringBtn(),
            userManagementBtn = this.getUserManagementBtn(),
            menuPanel = this.getMenuPanel();

        // 현재 선택된 item이 dashboardPanel일 경우 무시한다.
        if (centerContainer.layout.getActiveItem().itemId === "UserManagementPanel") {
            button.toggle(true);
            return;
        }

        dashboardBtn.toggle(false);
        managementBtn.toggle(false);
        monitoringBtn.toggle(false);
        userManagementBtn.toggle(true);

        centerContainer.layout.setActiveItem(3);

        Ext.getStore("UserStore").getProxy().url = GLOBAL.apiUrlPrefix + "user/list";
        Ext.getStore("UserStore").load();
    },

    onMytoolClick: function(tool, e, eOpts) {
        this.renderServerTree();
    },

    onMainContainerActivate: function(component, eOpts) {
        var listMenuPanel = this.getListMenuPanel();
        var centerContainer = this.getCenterContainer();

        centerContainer.layout.setActiveItem(0);

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

        Ext.getBody().mask("Loading...", "loading");

        this.renderServerTree();

    },

    onLnbLocationComboChange: function(field, newValue, oldValue, eOpts) {
        if(newValue != "") {
            Ext.getCmp("locationLabel").setText(newValue);

            menuConstants.me.renderServerTree();
        }
    },

    renderServerTree: function() {
        clearInterval(dashboardConstants.renderInterval);
        clearInterval(dashboardConstants.centerInterval);

        var center = Ext.getCmp("lnbLocationCombo").getValue();
        var treeData = [];

        dashboardConstants.me.setCenterStat();
        dashboardConstants.centerInterval = setInterval(function() {
            dashboardConstants.me.setCenterStat();
        }, 5000);

        Ext.Ajax.request({
            url: GLOBAL.apiUrlPrefix + 'mon/vmhost/_all?detail=true',
            disableCaching : true,
            success: function(response){

                var hostDatas = Ext.decode(response.responseText);

                menuConstants.hostRecord = hostDatas;

                if(hostDatas != null) {

                    var vmDatas = null;

                    Ext.Ajax.request({
                        url: GLOBAL.apiUrlPrefix + 'mon/vm/_all?detail=true',
                        disableCaching : true,
                        success: function(vmResponse){

                            vmDatas = Ext.decode(vmResponse.responseText);

                            menuConstants.vmRecord = vmDatas;

                            Ext.Ajax.request({
                                url: GLOBAL.apiUrlPrefix + 'mon/vm/all/status',
                                method : "GET",
                                disableCaching : true,
                                success: function(statResponse){

                                    if(statResponse.status == 200) {

                                        var statusDatas = Ext.decode(statResponse.responseText);

                                        renderTreeNode(hostDatas, vmDatas, statusDatas);
                                    } else {
                                        renderTreeNode(hostDatas, vmDatas, []);
                                    }
                                },
                                failure: function (response) {

                                    renderTreeNode(hostDatas, vmDatas, []);
                                }
                            });

                        }
                    });
                }

            },
            failure: function (response) {

                dashboardConstants.renderInterval = setInterval(function() {

                        menuConstants.me.renderServerTree();

                }, 10000);
            }
        });


        function renderTreeNode(hostDatas, vmDatas, statusDatas) {

            var extendsNodes = [];
            var nodes = Ext.getCmp("listMenuPanel").store.getRootNode().childNodes;
            for(var i=0; i<nodes.length; i++) {
                if(nodes[i].isExpanded()) {
                    extendsNodes.push(nodes[i].get("name"));
                }
            }

            menuConstants.selectionRecord = Ext.getCmp('listMenuPanel').getSelectionModel().getSelection();

            Ext.each(hostDatas, function(host, index) {

                if(host.location == center) {

                    host.id = host._id;
                    host.text = host.name;
                    host.icon = 'resources/images/icons/server.png';
                    host.type = 'vmhost';

                    Ext.each(host.info, function(hostInfo){
                        if(hostInfo.name == "Memory size") {
                            host.maxmem = parseInt(hostInfo.value.substring(0, hostInfo.value.length-4))*1024;
                        }
                    });

                    if(menuConstants.activeFlag) {
                        if(index == 0) {
                            host.expanded = true;
                        }
                        menuConstants.activeFlag = false;
                    } else {
                        for(var i=0; i<extendsNodes.length; i++) {
                            if(extendsNodes[i] == host.text) {
                                host.expanded = true;
                            }
                        }
                    }


                    var vmList = [];
                    Ext.each(vmDatas, function(vm) {

                        if(host._id == vm.vmhost) {

                            vm.id = vm._id;
                            vm.text = vm.vmname;
                            vm.icon = 'resources/images/icons/host.png';
                            vm.type = 'vm';
                            vm.leaf = true;
                            vm.cls = "node-red";
                            vm.interim = true;

                            Ext.each(statusDatas, function(hostStat, hostStatIdx) {

                                if(host.text === hostStat.vmhost) {

                                    Ext.each(hostStat.vms, function(vmStat){

                                        if(vmStat[vm.text]) {

                                            if(vmStat[vm.text] == "running") {
                                                vm.cls = "";
                                                vm.interim = false;

                                            } else if(vmStat[vm.text] == "shutoff") {
                                                vm.cls = "node-gray";
                                                vm.interim = false;

                                            } else if(vmStat[vm.text] == "interim") {
                                                vm.cls = "node-red";
                                                vm.interim = true;
                                            }
                                        }

                                    });
                                }
                            });

                            vmList.push(vm);
                        }
                    });

                    if(vmList.length > 0) {

                        host.leaf = false;
                        host.children = vmList;

                    } else {

                        host.leaf = true;

                    }

                    delete host.checked;

                    treeData.push(host);

                }

            });

            var treeStore = Ext.create('Ext.data.TreeStore', {
                storeId: 'mainTreeStore',
                model: 'spider.model.VmHostModel',
                root: {
                    expanded: true,
                    text: 'Server List',
                    icon : '',
                    type : 'root',
                    children: treeData
                }
            });

            Ext.getCmp("listMenuPanel").bindStore(treeStore);

            if(menuConstants.selectionRecord) {
                Ext.getCmp('listMenuPanel').getSelectionModel().select(menuConstants.selectionRecord,true,false);
            }

            dashboardConstants.me.renderDashboard();

            dashboardConstants.renderInterval = setInterval(function() {

                menuConstants.me.renderServerTree();

            }, 10000);

        }

    },

    renderVmStatus: function() {

        var treePanel = Ext.getCmp("listMenuPanel");

        Ext.Ajax.request({
            url: GLOBAL.apiUrlPrefix + 'mon/vm/all/status',
            method : "GET",
            disableCaching : true,
            success: function(response){

                if(response.status == 200) {

                    var datas = Ext.decode(response.responseText);

                    Ext.each(datas, function(host) {

                        var hostNodes = treePanel.store.getRootNode().childNodes;

                        Ext.each(hostNodes, function(record, idx){

                            if(host.vmhost === record.get("text")) {

                                var vmNodes = hostNodes[idx].childNodes;

                                Ext.each(vmNodes, function(vmRecord, vIdx){

                                    var cls = "node-red";

                                    Ext.each(host.vms, function(vm){

                                        if(vm[vmRecord.get("text")]) {
                                            if(vm[vmRecord.get("text")] == "running") {
                                                cls = "";
                                                vmRecord.set("interim", false);

                                            } else if(vm[vmRecord.get("text")] == "shutoff") {
                                                cls = "node-gray";
                                                vmRecord.set("interim", false);

                                            } else if(vm[vmRecord.get("text")] == "interim") {
                                                cls = "node-red";
                                                vmRecord.set("interim", true);
                                            }
                                        }

                                    });

                                    treePanel.getView().removeRowCls(vmNodes[vIdx], "node-gray");
                                    treePanel.getView().removeRowCls(vmNodes[vIdx], "node-red");
                                    treePanel.getView().addRowCls(vmNodes[vIdx], cls);

                                });


                            }

                        });

                    });

                }
            }
        });

    },

    init: function(application) {
                var menu = this;

                //Dashboard Menu Constants
                Ext.define('menuConstants', {
                    singleton: true,
                    me : menu,

                    hostRecord : null,
                    vmRecord : null,
                    selectionRecord : null,
                    activeFlag : true
                });

        this.control({
            "#dashboardBtn": {
                click: this.dashboardClick
            },
            "#managementBtn": {
                click: this.managementClick
            },
            "#monitoringBtn": {
                click: this.onMonitoringBtnClick
            },
            "#userManagementBtn": {
                click: this.onUserManagementBtnBtnClick
            },
            "#mytool": {
                click: this.onMytoolClick
            },
            "#mainContainer": {
                activate: this.onMainContainerActivate
            },
            "#lnbLocationCombo": {
                change: this.onLnbLocationComboChange
            }
        });
    },

    viewManagementMenu: function(record, tabIndex) {
        /**
         * NFV Management 메뉴 버튼 클릭 시 수행되는 function
         */
        var centerContainer = this.getCenterContainer(),
            dashboardBtn = this.getDashboardBtn(),
            managementBtn = this.getManagementBtn(),
            monitoringBtn = this.getMonitoringBtn(),
            userManagementBtn = this.getUserManagementBtn(),
            menuPanel = this.getMenuPanel();

        // 현재 선택된 item이 managementPanel일 경우 무시한다.
        if (centerContainer.layout.getActiveItem().itemId !== "VmManagementPanel") {

            managementBtn.toggle(true);
            dashboardBtn.toggle(false);
            monitoringBtn.toggle(false);
            userManagementBtn.toggle(false);

            centerContainer.layout.setActiveItem(1);

            if(record == null && vmConstants.selectRecord == null) {

                Ext.each(Ext.getCmp("listMenuPanel").store.getRootNode().childNodes, function(rec, idx){

                    Ext.each(rec.get("children"), function(cRecord, cIdx) {

                        record = cRecord;

                        return false;

                    });

                    if(record != null) {

                        var vmRecord = new spider.model.VmHostModel({
                            id			: record.id,
                            text		: record.text,
                            vmhostName	: record.vmhostName,
                            vmhost 		: record.vmhost
                        });

                        vmConstants.me.initVmManagement(vmRecord, tabIndex);

                        return false;
                    }

                });

            } else if(record != null) {
                vmConstants.me.initVmManagement(record, tabIndex);
            } else {
                vmConstants.me.initVmManagement(vmConstants.selectRecord, tabIndex);
            }


        } else {

            managementBtn.toggle(true);

            var vmDetailTab = Ext.getCmp("networkInstanceTabPanel");

            if(record.get("id") !== vmConstants.selectVmId) {

                vmConstants.me.initVmManagement(record, tabIndex);

            } else if(tabIndex == null && vmDetailTab.getActiveTab() !== vmDetailTab.items.getAt(0)) {

                vmConstants.me.initVmManagement(record, 0);

            } else if(tabIndex != null && vmDetailTab.getActiveTab() !== vmDetailTab.items.getAt(tabIndex)) {

                vmConstants.me.initVmManagement(record, tabIndex);
            }

        }

    },

    toggleDashboardBtn: function() {
        /**
         * Dashboard 메뉴 버튼 클릭 시 수행되는 function
         */
        var centerContainer = this.getCenterContainer(),
            dashboardBtn = this.getDashboardBtn(),
            managementBtn = this.getManagementBtn(),
            monitoringBtn = this.getMonitoringBtn(),
            userManagementBtn = this.getUserManagementBtn(),
            menuPanel = this.getMenuPanel();

        dashboardBtn.toggle(true);
        managementBtn.toggle(false);
        monitoringBtn.toggle(false);
        userManagementBtn.toggle(false);

        centerContainer.layout.setActiveItem(0);

    }

});
