/*
 * ***** BEGIN LICENSE BLOCK *****
 * Zimbra Collaboration Suite Server
 * Copyright (C) 2011 Zimbra Software, LLC.
 *
 * The contents of this file are subject to the Zimbra Public License
 * Version 1.4 ("License"); you may not use this file except in
 * compliance with the License.  You may obtain a copy of the License at
 * http://www.zimbra.com/license.
 *
 * Software distributed under the License is distributed on an "AS IS"
 * basis, WITHOUT WARRANTY OF ANY KIND, either express or implied.
 * ***** END LICENSE BLOCK *****
 */

#ifndef _NGX_MAIL_THROTTLE_H_INCLUDED_
#define _NGX_MAIL_THROTTLE_H_INCLUDED_

#include <ngx_core.h>
#include <ngx_event.h>
#include <ngx_mail.h>
#include <ngx_memcache.h>

struct ngx_mail_throttle_srv_conf_s {
    ngx_uint_t  mail_login_ip_max;
    ngx_msec_t  mail_login_ip_ttl;
    ngx_str_t   mail_login_ip_ttl_text;
    ngx_str_t   mail_login_ip_imap_ttl_text;
    ngx_str_t   mail_login_ip_pop3_ttl_text;
    ngx_str_t   mail_login_ip_rejectmsg;
    ngx_uint_t  mail_login_user_max;
    ngx_msec_t  mail_login_user_ttl;
    ngx_str_t   mail_login_user_ttl_text;
    ngx_str_t   mail_login_user_rejectmsg;
    ngx_uint_t  mail_login_ip_imap_max;
    ngx_msec_t  mail_login_ip_imap_ttl;
    ngx_uint_t  mail_login_ip_pop3_max;
    ngx_msec_t  mail_login_ip_pop3_ttl;
    ngx_array_t *mail_throttle_whitelist_ips;     /* array of ngx_cidr_t */

};
typedef struct ngx_mail_throttle_srv_conf_s ngx_mail_throttle_srv_conf_t;

struct throttle_callback_s;
typedef void (*throttle_handler_pt) (struct throttle_callback_s*);
typedef void * throttle_ctx_t;

struct throttle_callback_s {
    ngx_flag_t              check_only; /* whether just check the counter or increment it */
    ngx_mail_session_t     *session; /* current mail session */
    ngx_connection_t       *connection; /* current connection */
    ngx_event_t            *rev;    /* current read event */
    void                   *config; /* pointer to a configuration */
    ngx_log_t              *log;
    ngx_pool_t             *pool;
    throttle_handler_pt     on_allow; /* handler for allow access */
    throttle_handler_pt     on_deny;  /* handler for deny access */

    /* the following fields are used internally by throttle control */
    ngx_str_t              *user;           /* user name used by user throttle control */
    ngx_str_t              *ip;             /* ip address used by ip throttle control */
    ngx_str_t              *value;          /* the value for re-post memcache request */
    ngx_str_t              *key;            /* the key for re-post memcache request */
    ngx_str_t              *ttl;            /* the ttl value for re-post memcache request */
    ngx_str_t              *wl_key;         /* key for whitelist IP memcache add */
    ngx_uint_t              is_whitelisted; /* used by whitelist IP memcache callback */
};
typedef struct throttle_callback_s throttle_callback_t;

ngx_flag_t ngx_mail_throttle_init (ngx_mail_core_srv_conf_t *cscf);
void ngx_mail_throttle_ip (ngx_str_t ip, throttle_callback_t *callback);
void ngx_mail_throttle_whitelist_ip (ngx_str_t ip, throttle_callback_t *callback);
void ngx_mail_throttle_user (ngx_str_t user, throttle_callback_t *callback);
ngx_uint_t ngx_mail_throttle_ip_max_for_protocol (ngx_mail_throttle_srv_conf_t *tscf, ngx_uint_t protocol);

extern ngx_module_t ngx_mail_throttle_module;

#endif
