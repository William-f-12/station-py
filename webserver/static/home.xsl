<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:import href="layout.xsl"/>

    <xsl:template match="/">
        <xsl:call-template name="layout"/>
    </xsl:template>
    
    <xsl:template name="title">
        <link rel="stylesheet" href="/static/css/home.css"/>
        <title><xsl:value-of select="//head/title"/></title>
    </xsl:template>

    <xsl:template name="panel">
        <div class="outlines">
            <div><h2>Users</h2></div>
            <xsl:apply-templates select="//outline"/>
        </div>
    </xsl:template>

    <xsl:template name="main">
        <xsl:call-template name="form"/>
        <div id="headline_template">
            <div class="msg">
                <div>
                    <span class="timestamp">{{pubDate}}</span>
                </div>
                <div>
                    <a href="{{link}}">{{title}}</a>
                </div>
                <div class="desc">{{description}}</div>
            </div>
        </div>
        <div id="headlines">
            <div><h2>Messages</h2></div>
        </div>
        <script src="/static/js/home.js"/>
        <script src="anyone.js"/>
    </xsl:template>

    <xsl:template match="outline">
        <div class="user">
            <div class="name">
                <a>
                    <xsl:attribute name="href">
                        <xsl:value-of select="@xmlUrl"/>
                    </xsl:attribute>
                    <xsl:value-of select="@title"/>
                </a>
            </div>
        </div>
    </xsl:template>

    <xsl:template name="form">
        <script>
            function showRegister() {
                if (typeof dwitter.RegisterWindow !== 'function') {
                    alert('loading');
                    return;
                }
                dwitter.RegisterWindow.show();
            }
        </script>
        <div id="post_box">
            <div id="post_box_mask">
                <div>
                    <button onClick="javascript:showRegister();">Create Account</button>
                </div>
            </div>
            <div id="post_box_form">
                <textarea id="post_text"/>
                <span id="input_limit">bytes left</span>
                <button id="post_button">Submit</button>
            </div>
        </div>
    </xsl:template>

</xsl:stylesheet>