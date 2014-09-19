/*
 * File: app/view/MyPanel93.js
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

Ext.define('spider.view.MyPanel93', {
    extend: 'Ext.panel.Panel',

    requires: [
        'spider.view.MyPanel31',
        'Ext.panel.Panel'
    ],

    id: 'dashboardPanel1',
    itemId: 'dashboardPanel1',
    autoScroll: true,
    layout: 'column',

    initComponent: function() {
        var me = this;

        Ext.applyIf(me, {
            items: [
                {
                    xtype: 'mypanel31',
                    columnWidth: 0.5
                },
                {
                    xtype: 'mypanel31',
                    columnWidth: 0.5
                }
            ]
        });

        me.callParent(arguments);
    }

});