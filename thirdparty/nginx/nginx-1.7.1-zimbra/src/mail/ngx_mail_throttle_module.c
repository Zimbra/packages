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

#include <arpa/inet.h>
#include <ngx_mail_throttle_module.h>
#include <ngx_zm_lookup.h>
#include <ngx_memcache.h>

static ngx_str_t throttle_zero = ngx_string("0");

static void *ngx_mail_throttle_create_srv_conf
    (ngx_conf_t *cf);
static char *ngx_mail_throttle_merge_srv_conf
    (ngx_conf_t *cf, void *parent, void *child);
static char *ngx_mail_throttle_ip_ttl
    (ngx_conf_t *cf, ngx_command_t* command, void * conf);
static char *ngx_mail_throttle_ip_imap_ttl
    (ngx_conf_t *cf, ngx_command_t* command, void * conf);
static char *ngx_mail_throttle_ip_pop3_ttl
    (ngx_conf_t *cf, ngx_command_t* command, void * conf);
static char *ngx_mail_throttle_user_ttl
    (ngx_conf_t *cf, ngx_command_t* command, void * conf);
static char *ngx_mail_throttle_set_ttl_text
    (ngx_msec_t ttl, ngx_str_t * input, ngx_str_t * ttl_text);
static char *ngx_mail_throttle_whitelist_ips
    (ngx_conf_t *cf, ngx_command_t *cmd, void *conf);
void ngx_mail_throttle_whitelist_lookup_ip
    (throttle_callback_t *callback);
static void ngx_mail_throttle_whitelist_lookup_ip_success_handler
    (mc_work_t *w);
static void ngx_mail_throttle_whitelist_lookup_ip_failure_handler
    (mc_work_t *w);
static void ngx_mail_throttle_ip_success_handler
    (mc_work_t *w);
static void ngx_mail_throttle_ip_failure_handler
    (mc_work_t *w);
static void ngx_mail_throttle_whitelist_ip_success_handler
    (mc_work_t *w);
static void ngx_mail_throttle_whitelist_ip_failure_handler
    (mc_work_t *w);
static ngx_str_t ngx_mail_throttle_ip_ttl_txt
    (ngx_mail_throttle_srv_conf_t * tscf, ngx_uint_t protocol);
static void ngx_mail_throttle_ip_add
    (ngx_str_t *ip, throttle_callback_t *callback);
static void ngx_mail_throttle_ip_add_success_handler
    (mc_work_t *w);
static void ngx_mail_throttle_ip_add_failure_handler
    (mc_work_t *w);
static void ngx_mail_throttle_quser
    (ngx_str_t *quser, throttle_callback_t *callback);
static void ngx_mail_throttle_quser_success_handler
    (mc_work_t *w);
static void ngx_mail_throttle_quser_failure_handler
    (mc_work_t *w);
static void ngx_mail_throttle_user_add
    (ngx_str_t *user, throttle_callback_t *callback);
static void ngx_mail_throttle_user_add_success_handler
    (mc_work_t *w);
static void ngx_mail_throttle_user_add_failure_handler
    (mc_work_t *w);
static void ngx_mail_throttle_user_success_handler
    (mc_work_t *w);
static void ngx_mail_throttle_user_failure_handler
    (mc_work_t *w);
static ngx_str_t ngx_mail_throttle_get_ip_throttle_key
   (ngx_pool_t *pool, ngx_log_t *log, ngx_str_t ip, ngx_uint_t protocol);
static ngx_str_t ngx_mail_throttle_get_ip_whitelist_key
   (ngx_pool_t *pool, ngx_log_t *log, ngx_str_t ip);
static ngx_str_t ngx_mail_throttle_get_user_throttle_key
   (ngx_pool_t *pool, ngx_log_t *log, ngx_str_t user);
static char * ngx_encode_protocol
   (ngx_uint_t protocol, char eptype);

static ngx_command_t  ngx_mail_throttle_commands[] = {
    { ngx_string("mail_login_ip_max"),
      NGX_MAIL_MAIN_CONF|NGX_CONF_TAKE1,
      ngx_conf_set_num_slot,
      NGX_MAIL_SRV_CONF_OFFSET,
      offsetof(ngx_mail_throttle_srv_conf_t, mail_login_ip_max),
      NULL },

    { ngx_string("mail_login_ip_ttl"),
      NGX_MAIL_MAIN_CONF|NGX_CONF_TAKE1,
      ngx_mail_throttle_ip_ttl,
      NGX_MAIL_SRV_CONF_OFFSET,
      offsetof(ngx_mail_throttle_srv_conf_t, mail_login_ip_ttl),
      NULL },

    { ngx_string("mail_login_ip_rejectmsg"),
      NGX_MAIL_MAIN_CONF|NGX_CONF_TAKE1,
      ngx_conf_set_str_slot,
      NGX_MAIL_SRV_CONF_OFFSET,
      offsetof(ngx_mail_throttle_srv_conf_t, mail_login_ip_rejectmsg),
      NULL },

    { ngx_string("mail_login_user_max"),
      NGX_MAIL_MAIN_CONF|NGX_CONF_TAKE1,
      ngx_conf_set_num_slot,
      NGX_MAIL_SRV_CONF_OFFSET,
      offsetof(ngx_mail_throttle_srv_conf_t, mail_login_user_max),
      NULL },

    { ngx_string("mail_login_user_ttl"),
      NGX_MAIL_MAIN_CONF|NGX_CONF_TAKE1,
      ngx_mail_throttle_user_ttl,
      NGX_MAIL_SRV_CONF_OFFSET,
      offsetof(ngx_mail_throttle_srv_conf_t, mail_login_user_ttl),
      NULL },

    { ngx_string("mail_login_user_rejectmsg"),
      NGX_MAIL_MAIN_CONF|NGX_CONF_TAKE1,
      ngx_conf_set_str_slot,
      NGX_MAIL_SRV_CONF_OFFSET,
      offsetof(ngx_mail_throttle_srv_conf_t, mail_login_user_rejectmsg),
      NULL },

    { ngx_string("mail_login_ip_imap_max"),
      NGX_MAIL_MAIN_CONF|NGX_CONF_TAKE1,
      ngx_conf_set_num_slot,
      NGX_MAIL_SRV_CONF_OFFSET,
      offsetof(ngx_mail_throttle_srv_conf_t, mail_login_ip_imap_max),
      NULL },

    { ngx_string("mail_login_ip_imap_ttl"),
      NGX_MAIL_MAIN_CONF|NGX_CONF_TAKE1,
      ngx_mail_throttle_ip_imap_ttl,
      NGX_MAIL_SRV_CONF_OFFSET,
      offsetof(ngx_mail_throttle_srv_conf_t, mail_login_ip_imap_ttl),
      NULL },

    { ngx_string("mail_login_ip_pop3_max"),
      NGX_MAIL_MAIN_CONF|NGX_CONF_TAKE1,
      ngx_conf_set_num_slot,
      NGX_MAIL_SRV_CONF_OFFSET,
      offsetof(ngx_mail_throttle_srv_conf_t, mail_login_ip_pop3_max),
      NULL },

    { ngx_string("mail_login_ip_pop3_ttl"),
      NGX_MAIL_MAIN_CONF|NGX_CONF_TAKE1,
      ngx_mail_throttle_ip_pop3_ttl,
      NGX_MAIL_SRV_CONF_OFFSET,
      offsetof(ngx_mail_throttle_srv_conf_t, mail_login_ip_pop3_ttl),
      NULL },

    { ngx_string("mail_whitelist_ip"),
      NGX_MAIL_MAIN_CONF|NGX_CONF_1MORE,
      ngx_mail_throttle_whitelist_ips,
      NGX_MAIL_SRV_CONF_OFFSET,
      offsetof(ngx_mail_throttle_srv_conf_t, mail_throttle_whitelist_ips),
      NULL },

     ngx_null_command
};

static ngx_mail_module_t  ngx_mail_throttle_module_ctx = {
    NULL,                                  /* protocol */
    NULL,                                  /* create main configuration */
    NULL,                                  /* init main configuration */

    ngx_mail_throttle_create_srv_conf,     /* create server configuration */
    ngx_mail_throttle_merge_srv_conf       /* merge server configuration */
};

ngx_module_t  ngx_mail_throttle_module = {
    NGX_MODULE_V1,
    &ngx_mail_throttle_module_ctx,         /* module context */
    ngx_mail_throttle_commands,            /* module directives */
    NGX_MAIL_MODULE,                       /* module type */
    NULL,                                  /* init master */
    NULL,                                  /* init module */
    NULL,                                  /* init process */
    NULL,                                  /* init thread */
    NULL,                                  /* exit thread */
    NULL,                                  /* exit process */
    NULL,                                  /* exit master */
    NGX_MODULE_V1_PADDING
};

static void *
ngx_mail_throttle_create_srv_conf(ngx_conf_t *cf)
{
    ngx_mail_throttle_srv_conf_t  *tscf;

    tscf = ngx_pcalloc(cf->pool, sizeof(ngx_mail_throttle_srv_conf_t));
    if (tscf == NULL) {
        return NULL;
    }

    tscf->mail_login_ip_max = NGX_CONF_UNSET;
    tscf->mail_login_ip_imap_max = NGX_CONF_UNSET;
    tscf->mail_login_ip_pop3_max = NGX_CONF_UNSET;
    tscf->mail_login_ip_ttl = NGX_CONF_UNSET_MSEC;
    tscf->mail_login_ip_imap_ttl = NGX_CONF_UNSET_MSEC;
    tscf->mail_login_ip_pop3_ttl = NGX_CONF_UNSET_MSEC;
    ngx_str_null (&tscf->mail_login_ip_ttl_text);
    ngx_str_null (&tscf->mail_login_ip_imap_ttl_text);
    ngx_str_null (&tscf->mail_login_ip_pop3_ttl_text);
    tscf->mail_login_user_max = NGX_CONF_UNSET;
    tscf->mail_login_user_ttl = NGX_CONF_UNSET_MSEC;
    ngx_str_null (&tscf->mail_login_user_ttl_text);
    tscf->mail_throttle_whitelist_ips = NGX_CONF_UNSET_PTR;

    return tscf;
}

static char *
ngx_mail_throttle_merge_srv_conf(ngx_conf_t *cf, void *parent, void *child)
{
    ngx_mail_throttle_srv_conf_t *prev = parent;
    ngx_mail_throttle_srv_conf_t *conf = child;

    ngx_conf_merge_uint_value (conf->mail_login_ip_max,
                               prev->mail_login_ip_max, 1000);
    ngx_conf_merge_uint_value (conf->mail_login_ip_imap_max,
                               prev->mail_login_ip_imap_max, 0);
    ngx_conf_merge_uint_value (conf->mail_login_ip_pop3_max,
                               prev->mail_login_ip_pop3_max, 0);
    ngx_conf_merge_uint_value (conf->mail_login_user_max,
                               prev->mail_login_user_max, 100);
    ngx_conf_merge_msec_value (conf->mail_login_ip_ttl,
                               prev->mail_login_ip_ttl, 60000);
    ngx_conf_merge_msec_value (conf->mail_login_ip_imap_ttl,
                               prev->mail_login_ip_imap_ttl, 60000);
    ngx_conf_merge_msec_value (conf->mail_login_ip_pop3_ttl,
                               prev->mail_login_ip_pop3_ttl, 60000);
    ngx_conf_merge_msec_value (conf->mail_login_user_ttl,
                               prev->mail_login_user_ttl, 60000);
    ngx_conf_merge_str_value (conf->mail_login_ip_rejectmsg,
                              prev->mail_login_ip_rejectmsg, "");
    ngx_conf_merge_str_value (conf->mail_login_user_rejectmsg,
                              prev->mail_login_user_rejectmsg, "");
    ngx_conf_merge_str_value (conf->mail_login_ip_ttl_text,
                              prev->mail_login_ip_ttl_text, "60");
    ngx_conf_merge_str_value (conf->mail_login_ip_imap_ttl_text,
                              prev->mail_login_ip_imap_ttl_text, "60");
    ngx_conf_merge_str_value (conf->mail_login_ip_pop3_ttl_text,
                              prev->mail_login_ip_pop3_ttl_text, "60");
    ngx_conf_merge_str_value (conf->mail_login_user_ttl_text,
                              prev->mail_login_user_ttl_text, "60");

    ngx_conf_merge_ptr_value(conf->mail_throttle_whitelist_ips,
                             prev->mail_throttle_whitelist_ips,
                             NGX_CONF_UNSET_PTR);

    return NGX_CONF_OK;
}

static char *
ngx_mail_throttle_ip_ttl (ngx_conf_t *cf, ngx_command_t *cmd, void *conf) {
    char      *res;
    ngx_str_t *value;
    ngx_mail_throttle_srv_conf_t *tscf = conf;

    res = ngx_conf_set_msec_slot(cf, cmd, conf);

    if (res != NGX_CONF_OK) {
        return res;
    }

    value = cf->args->elts;
    res = ngx_mail_throttle_set_ttl_text (tscf->mail_login_ip_ttl,
                    &value[1], &tscf->mail_login_ip_ttl_text);

    if (res != NGX_CONF_OK) {
        return res;
    }

    return NGX_CONF_OK;
}

static char *
ngx_mail_throttle_ip_imap_ttl (ngx_conf_t *cf, ngx_command_t *cmd, void *conf) {
    char      *res;
    ngx_str_t *value;
    ngx_mail_throttle_srv_conf_t *tscf = conf;

    res = ngx_conf_set_msec_slot(cf, cmd, conf);

    if (res != NGX_CONF_OK) {
        return res;
    }

    value = cf->args->elts;
    res = ngx_mail_throttle_set_ttl_text (tscf->mail_login_ip_imap_ttl,
                    &value[1], &tscf->mail_login_ip_imap_ttl_text);

    if (res != NGX_CONF_OK) {
        return res;
    }

    return NGX_CONF_OK;
}

static char *
ngx_mail_throttle_ip_pop3_ttl (ngx_conf_t *cf, ngx_command_t *cmd, void *conf) {
    char      *res;
    ngx_str_t *value;
    ngx_mail_throttle_srv_conf_t *tscf = conf;

    res = ngx_conf_set_msec_slot(cf, cmd, conf);

    if (res != NGX_CONF_OK) {
        return res;
    }

    value = cf->args->elts;
    res = ngx_mail_throttle_set_ttl_text (tscf->mail_login_ip_pop3_ttl,
                    &value[1], &tscf->mail_login_ip_pop3_ttl_text);

    if (res != NGX_CONF_OK) {
        return res;
    }

    return NGX_CONF_OK;
}

static char *
ngx_mail_throttle_user_ttl (ngx_conf_t *cf, ngx_command_t *cmd, void *conf) {
    char      *res;
    ngx_str_t *value;
    ngx_mail_throttle_srv_conf_t *tscf = conf;

    res = ngx_conf_set_msec_slot(cf, cmd, conf);

    if (res != NGX_CONF_OK) {
        return res;
    }

    value = cf->args->elts;
    res = ngx_mail_throttle_set_ttl_text (tscf->mail_login_user_ttl,
                    &value[1], &tscf->mail_login_user_ttl_text);

    if (res != NGX_CONF_OK) {
        return res;
    }

    return NGX_CONF_OK;
}

static char *
ngx_mail_throttle_set_ttl_text (ngx_msec_t ttl, ngx_str_t * input, ngx_str_t * ttl_text) {

   if (ttl > 1000) {
       if (input->len > 2 &&
           input->data[input->len - 2] == 'm' &&
           input->data[input->len - 1] == 's') {
           /* for ms value, trim the last 5 characters 'NNNms' and become the number of seconds
            * for example, 3600000ms --> 3600 */
           ttl_text->data = input->data;
           ttl_text->len = input->len - 5;
       } else {
           /* no trailing "ms", directly used as second value */
           *ttl_text = *input;
       }
   } else if (ttl > 0) {
       /* 0 ~ 1000ms, make it 1 */
       ngx_str_set(ttl_text, "1");
   } else if (ttl == 0){
       ngx_str_set(ttl_text, "0");
   } else {
       return "invalid value";
   }

   return NGX_CONF_OK;
}

static char *
ngx_mail_throttle_whitelist_ips (ngx_conf_t *cf, ngx_command_t *cmd, void *conf) {
    ngx_cidr_t                   *cidr;
    ngx_mail_throttle_srv_conf_t *tscf = conf;
    ngx_uint_t                    i;
    ngx_int_t                     rc;
    ngx_str_t                     *value;

    if (tscf->mail_throttle_whitelist_ips == NGX_CONF_UNSET_PTR) {
	// This function gets called once for each mail_whitelist_ip parameter/value found.
        // TODO - see if there is a way to determine here how many of these there are so that
        //        we can allocate the exact number of elements that we need at once.
        tscf->mail_throttle_whitelist_ips = ngx_array_create(cf->pool, 10, sizeof(ngx_cidr_t));
        if (tscf->mail_throttle_whitelist_ips == NGX_CONF_UNSET_PTR) {
            return NGX_CONF_ERROR;
        }
    }

    for (i = 1; i < cf->args->nelts; ++i)
    {
        value = &((ngx_str_t *)cf->args->elts)[i];
        cidr = ngx_array_push(tscf->mail_throttle_whitelist_ips);
        if (cidr == NULL) {
            return NGX_CONF_ERROR;
        }
        rc = ngx_ptocidr(value, cidr);
        if (rc == NGX_ERROR) {
            ngx_conf_log_error(NGX_LOG_EMERG, cf, 0, "invalid mail_whitelist_ip parameter \"%V\"", &value[1]);
            return NGX_CONF_ERROR;
        }
    }

    return NGX_CONF_OK;
}

void
ngx_mail_throttle_whitelist_lookup_ip (throttle_callback_t *callback) {
    mc_work_t                        w;
    ngx_int_t                        i;
    ngx_cidr_t                       ip_cidr, *cidr;
    ngx_log_t                       *log;
    ngx_uint_t                       rc;
    ngx_mail_session_t              *session;
    ngx_mail_throttle_srv_conf_t    *tscf;
    ngx_pool_t                      *pool;
    ngx_str_t                        *ip, *cache_val, tmpval;

    ip = callback->ip;
    callback->is_whitelisted = 0;
    log = callback->log;
    pool = callback->pool;
    session = callback->session;

    tscf = ngx_mail_get_module_srv_conf(session, ngx_mail_throttle_module);
    if (tscf->mail_throttle_whitelist_ips == NGX_CONF_UNSET_PTR) {
        ngx_log_error (NGX_LOG_DEBUG, log, 0, "no whitelisted ips, %V not whitelisted", ip);
        ngx_mail_throttle_ip(*ip, callback);
        return;
    }
    rc = ngx_ptocidr(ip, &ip_cidr);
    if (rc == NGX_ERROR) {
        ngx_log_error (NGX_LOG_ERR, log, 0, "whitelisting ip %V do to error converting to cidr", ip);
        ngx_mail_throttle_ip(*ip, callback);
        return;
    }
#if (NGX_HAVE_INET6)
    if (ip_cidr.family == AF_INET6) {
        ngx_log_debug1(NGX_LOG_DEBUG_MAIL, log, 0, "ngx_mail_throttle_ip_whitelisted: %V is IPV6", ip);
        for (i = 0; i < tscf->mail_throttle_whitelist_ips->nelts; ++i) {
            cidr = &((ngx_cidr_t *)tscf->mail_throttle_whitelist_ips->elts)[i];
            if (cidr->family == AF_INET6) {
                if (
                    ((ip_cidr.u.in6.addr.__in6_u.__u6_addr32[0] & cidr->u.in6.mask.__in6_u.__u6_addr32[0]) ==
                     (cidr->u.in6.addr.__in6_u.__u6_addr32[0] & cidr->u.in6.mask.__in6_u.__u6_addr32[0])) &&
                    ((ip_cidr.u.in6.addr.__in6_u.__u6_addr32[1] & cidr->u.in6.mask.__in6_u.__u6_addr32[1]) ==
                     (cidr->u.in6.addr.__in6_u.__u6_addr32[1] & cidr->u.in6.mask.__in6_u.__u6_addr32[1])) &&
                    ((ip_cidr.u.in6.addr.__in6_u.__u6_addr32[2] & cidr->u.in6.mask.__in6_u.__u6_addr32[2]) ==
                     (cidr->u.in6.addr.__in6_u.__u6_addr32[2] & cidr->u.in6.mask.__in6_u.__u6_addr32[2])) &&
                    ((ip_cidr.u.in6.addr.__in6_u.__u6_addr32[3] & cidr->u.in6.mask.__in6_u.__u6_addr32[3]) ==
                     (cidr->u.in6.addr.__in6_u.__u6_addr32[3] & cidr->u.in6.mask.__in6_u.__u6_addr32[3]))
                   ) {
                    ngx_log_debug1(NGX_LOG_DEBUG_MAIL, log, 0, "ngx_mail_throttle_ip_whitelisted: IPV6: %V is whitelisted", ip);
                    callback->is_whitelisted = 1;
                }
            }
        }
    }
#endif
    if (ip_cidr.family == AF_INET) {
        ngx_log_debug1(NGX_LOG_DEBUG_MAIL, log, 0, "ngx_mail_throttle_ip_whitelisted: %V is IPV4", ip);
        for (i = 0; i < tscf->mail_throttle_whitelist_ips->nelts; ++i) {
            cidr = &((ngx_cidr_t *)tscf->mail_throttle_whitelist_ips->elts)[i];
            if (cidr->family == AF_INET) {
                ngx_log_debug1(NGX_LOG_DEBUG_MAIL, log, 0, "ngx_mail_throttle_ip_whitelisted: verify IPV4: %V", ip);
                if ((ip_cidr.u.in.addr & cidr->u.in.mask) == (cidr->u.in.addr & cidr->u.in.mask)) {
                    ngx_log_debug1(NGX_LOG_DEBUG_MAIL, log, 0, "ngx_mail_throttle_ip_whitelisted: IPV4: %V is whitelisted", ip);
                    callback->is_whitelisted = 1;
                }
            }
        }
    }

    tmpval.len = 1;
    tmpval.data = callback->is_whitelisted ? "1" : "0";
    cache_val = ngx_pstrcpy(pool, &tmpval);
    if (cache_val == NULL) {
        ngx_log_error (NGX_LOG_ERR, log, 0,
            "Unable to cache fact that %V is_whitelisted=%d (alloc mem for cache_val)",
            ip, callback->is_whitelisted);
        if (callback->is_whitelisted) {
            callback->on_allow(callback);
        }
        else {
            ngx_mail_throttle_ip(*ip, callback);
        }
        return;
    }

    w.ctx = callback;
    w.request_code = mcreq_add;
    w.response_code = mcres_unknown;
    w.on_success = ngx_mail_throttle_whitelist_lookup_ip_success_handler;
    w.on_failure = ngx_mail_throttle_whitelist_lookup_ip_failure_handler;

    ngx_memcache_post(&w, *callback->wl_key, *cache_val, NULL, log);
}

static void
ngx_mail_throttle_whitelist_lookup_ip_success_handler (mc_work_t *w) {
    ngx_log_t               *log;
    throttle_callback_t     *callback;

    callback = (throttle_callback_t *)w->ctx;
    log = callback->log;

    ngx_log_debug2(NGX_LOG_DEBUG_MAIL, log, 0, "cached is_whitelisted=%d for IP %V", callback->is_whitelisted, callback->ip);

    if (callback->is_whitelisted) {
        callback->on_allow(callback);
    }
    else {
        ngx_mail_throttle_ip(*callback->ip, callback);
    }
}

static void
ngx_mail_throttle_whitelist_lookup_ip_failure_handler (mc_work_t *w) {
    ngx_log_t               *log;
    throttle_callback_t     *callback;

    callback = (throttle_callback_t *)w->ctx;
    log = callback->log;

    ngx_log_error (NGX_LOG_NOTICE, log, 0, "error trying to cache whitelist status for IP %V", callback->ip);
    if (callback->is_whitelisted) {
        callback->on_allow(callback);
    }
    else {
        ngx_mail_throttle_ip(*callback->ip, callback);
    }
}

/* check whether the client ip should be allowed to proceed, or whether
   the connection should be throttled
 */
void ngx_mail_throttle_ip (ngx_str_t ip, throttle_callback_t *callback)
{
    ngx_log_t       *log;
    ngx_pool_t      *pool;
    mc_work_t        w;
    ngx_str_t        k;
    ngx_str_t       *value, *eip, *key;
    ngx_uint_t       protocol;

    pool = callback->pool;
    log = callback->log;
    protocol = callback->session->protocol;

    ngx_log_debug2(NGX_LOG_DEBUG_MAIL, log, 0, "check ip throttle:[%s, %V]", ngx_encode_protocol(protocol, 'l'), &ip);

    w.ctx = callback;
    w.request_code = mcreq_incr;
    w.response_code = mcres_unknown;
    w.on_success = ngx_mail_throttle_ip_success_handler;
    w.on_failure = ngx_mail_throttle_ip_failure_handler;

    k = ngx_mail_throttle_get_ip_throttle_key(pool, log, ip, protocol);

    if (k.len == 0) {
        ngx_log_error (NGX_LOG_ERR, log, 0,
                "allowing ip %V login because of internal error"
                "in ip throttle control (generate key for incr)", &ip);
        callback->on_allow(callback);
        return;
    }

    key = ngx_pstrcpy (pool, &k);
    if (key == NULL) {
        ngx_log_error (NGX_LOG_ERR, log, 0,
                "allowing ip %V login because of internal error"
                "in ip throttle control (deep copy key for incr)", &ip);
        callback->on_allow(callback);
    }

    value = ngx_palloc (pool, sizeof(ngx_str_t));
    if (value == NULL) {
        ngx_log_error (NGX_LOG_ERR, log, 0,
                "allowing ip %V login because of internal error"
                "in ip throttle control (alloc mem for incr value)", &ip);
        callback->on_allow(callback);
        return;
    }

    ngx_str_set(value, "1");

    /* make a copy of the input IP address for callback reference */
    eip = ngx_pstrcpy (pool, &ip);
    if (eip == NULL) {
        ngx_log_error (NGX_LOG_ERR, log, 0,
                "allowing ip %V login because of internal error"
                "in ip throttle control (deep copy ip for incr)", &ip);
        callback->on_allow(callback);
        return;
    }

    callback->ip = eip;
    callback->value = value;
    callback->key = key;

    ngx_memcache_post(&w, *key, *value, /* pool */ NULL, log);
}

ngx_uint_t ngx_mail_throttle_ip_max_for_protocol (
    ngx_mail_throttle_srv_conf_t * tscf,
    ngx_uint_t protocol
)
{
    ngx_uint_t login_ip_max = 0;

    switch (protocol) {
        case NGX_MAIL_POP3_PROTOCOL:
            login_ip_max = tscf->mail_login_ip_pop3_max > 0 ? tscf->mail_login_ip_pop3_max : tscf->mail_login_ip_max;
            break;
        case NGX_MAIL_IMAP_PROTOCOL:
            login_ip_max = tscf->mail_login_ip_imap_max > 0 ? tscf->mail_login_ip_imap_max : tscf->mail_login_ip_max;
            break;
        default:
            login_ip_max = tscf->mail_login_ip_max;
    }
    return login_ip_max;
}

/* memcache handler (return counter for the specified ip or NOT_FOUND) */
static void ngx_mail_throttle_ip_success_handler (mc_work_t *w)
{
    ngx_mail_throttle_srv_conf_t * tscf;
    throttle_callback_t     *callback = w->ctx;
    ngx_mail_session_t  *s  = callback->session;
    ngx_str_t                ip = *callback->ip;
    size_t                   hits;
    ngx_str_t                counter;
    ngx_uint_t		     login_ip_max;

    /* the increment was successful - deep copy w->payload to counter */
    counter.data = ngx_pstrdup (callback->pool, &w->payload);

    if (counter.data == NULL) {
        /* enomem */
        counter = throttle_zero;    /* "0" */
    } else {
        counter.len = w->payload.len;
    }

    /* check if the limit has exceeded */
    ngx_log_debug2(NGX_LOG_DEBUG_MAIL, callback->log, 0,
        "ip throttle:%V is %V", &ip, &counter);

    hits = ngx_atoi(counter.data, counter.len);

    tscf = ngx_mail_get_module_srv_conf(s, ngx_mail_throttle_module);
    login_ip_max = ngx_mail_throttle_ip_max_for_protocol(tscf, s->protocol);
    ngx_log_error (NGX_LOG_DEBUG, callback->log, 0,
        "ngx_mail_throttle_ip_success_handler: login_ip_max=%d, mail_login_ip_max=%d, "
        "mail_login_ip_imap_max=%d, mail_login_ip_pop3_max=%d",
        login_ip_max, tscf->mail_login_ip_max, tscf->mail_login_ip_imap_max, tscf->mail_login_ip_pop3_max);

    if (login_ip_max == 0) {
        //should never reach here because mail handler won't
        //start throttle control if it's unlimited.
        ngx_log_error (NGX_LOG_INFO, callback->log, 0,
            "ip throttle:[%V] allow [count:%d, limit:inf]",
            &ip, hits);
        callback->on_allow(callback);
    } else if (hits <= login_ip_max) {
        ngx_log_error (NGX_LOG_INFO, callback->log, 0,
            "ip throttle:[%V] allow [count:%d, limit:%d]",
            &ip, hits, login_ip_max);
        callback->on_allow(callback);
    } else {
        ngx_log_error (NGX_LOG_NOTICE, callback->log, 0,
            "ip throttle:[%V] deny [count:%d, limit:%d]",
            &ip, hits, login_ip_max);
        callback->on_deny(callback);
    }
}

static void ngx_mail_throttle_ip_failure_handler (mc_work_t *w)
{
    throttle_callback_t  *callback = w->ctx;
    ngx_log_t            *log = callback->log;
    if (w->response_code == mcres_failure_normal) {
        /* increment failed, we must begin to add counter for this ip */
        ngx_log_debug1(NGX_LOG_DEBUG_MAIL, log, 0,
            "ip throttle:%V create counter", callback->ip);
        ngx_mail_throttle_ip_add (callback->ip, callback);

    } else if (w->response_code == mcres_failure_again) {
        mc_work_t nw; /* create a new work entry */
        nw.ctx = callback;
        nw.request_code = mcreq_incr;
        nw.response_code = mcres_unknown;
        nw.on_success = ngx_mail_throttle_ip_success_handler;
        nw.on_failure = ngx_mail_throttle_ip_failure_handler;
        ngx_log_error (NGX_LOG_NOTICE, log, 0,
                "retry to check ip throttle:[%V]", callback->ip);
        ngx_memcache_post(&nw, *callback->key, *callback->value,
                          /* pool */ NULL, log);

    } else { /* mcres_failure_unavailable */
        ngx_log_error (NGX_LOG_ERR, log, 0,
             "throttle allowing access from ip %V because of "
             "memcache service is unavailable when try to "
             "increment ip counter", callback->ip);
        callback->on_allow(callback);
    }
}

/* check cache to see whether the client ip is whitelisted.  if so,
   invokes callback->on_allow.  if not, calls ngx_mail_throttle_ip.
   If no IPs are configured for whitelisting, doesn't bother checking
   cache and just calls ngx_mail_throttle_ip.
 */
void
ngx_mail_throttle_whitelist_ip (ngx_str_t ip, throttle_callback_t *callback) {
    ngx_log_t                       *log;
    ngx_mail_session_t              *session;
    ngx_mail_throttle_srv_conf_t    *tscf;
    ngx_pool_t                      *pool;
    mc_work_t                        w;
    ngx_str_t                        k;
    ngx_str_t                       *value, *eip, *key;

    pool = callback->pool;
    log = callback->log;
    session = callback->session;
    tscf = ngx_mail_get_module_srv_conf(session, ngx_mail_throttle_module);
    if (tscf->mail_throttle_whitelist_ips == NGX_CONF_UNSET_PTR) {
        ngx_log_debug1(NGX_LOG_DEBUG_MAIL, log, 0, "no configured whitelisted IPs, %V not whitelisted", &ip);
        ngx_mail_throttle_ip(ip, callback);
        return;
    }

    k = ngx_mail_throttle_get_ip_whitelist_key (pool, log, ip);
    if (k.len == 0) {
        ngx_log_error (NGX_LOG_ERR, log, 0,
                "allowing ip %V login because of internal error"
                "in ip throttle whitelist control (generate key for get)", &ip);
        callback->on_allow(callback);
        return;
    }
    key = ngx_pstrcpy (pool, &k);
    if (key == NULL) {
        ngx_log_error (NGX_LOG_ERR, log, 0,
                "allowing ip %V login because of internal error"
                "in ip throttle whitelist control (deep copy key for get)", &ip);
        callback->on_allow(callback);
    }
    /* make a copy of the input IP address for callback reference */
    eip = ngx_pstrcpy (pool, &ip);
    if (eip == NULL) {
        ngx_log_error (NGX_LOG_ERR, log, 0,
                "allowing ip %V login because of internal error"
                "in ip throttle whitelist control (deep copy ip for get)", &ip);
        callback->on_allow(callback);
        return;
    }

    callback->ip = eip;
    callback->wl_key = key;

    w.ctx = callback;
    w.request_code = mcreq_get;
    w.response_code = mcres_unknown;
    w.on_success = ngx_mail_throttle_whitelist_ip_success_handler;
    w.on_failure = ngx_mail_throttle_whitelist_ip_failure_handler;

    ngx_memcache_post(&w, *key, NGX_EMPTY_STR,/* pool */ NULL, log);
}

static void
ngx_mail_throttle_whitelist_ip_success_handler (mc_work_t *w) {
    ngx_log_t           *log;
    ngx_pool_t          *pool;
    throttle_callback_t *callback;

    callback = (throttle_callback_t *)w->ctx;
    log = callback->log;
    pool = callback->pool;

    if (w->payload.len > 0) {
        if (w->payload.data[0] == '1') {
            ngx_log_debug1(NGX_LOG_DEBUG_MAIL, log, 0, "ip %V whitelisted (from cache)", callback->ip);
            callback->on_allow(callback);
            return;
        }
        else {
            ngx_log_debug1(NGX_LOG_DEBUG_MAIL, log, 0, "ip %V is not whitelisted (from cache)", callback->ip);
            ngx_mail_throttle_ip(*callback->ip, callback);
            return;
        }
    }
    else {
        ngx_mail_throttle_whitelist_lookup_ip(callback);
    }
}

static void
ngx_mail_throttle_whitelist_ip_failure_handler (mc_work_t *w) {

    ngx_log_t           *log;
    throttle_callback_t *callback;

    callback = (throttle_callback_t *)w->ctx;
    log = callback->log;

    if (w->response_code == mcres_failure_normal) {
        // NOT FOUND
        ngx_log_debug1(NGX_LOG_DEBUG_MAIL, log, 0, "whitelist status for IP %V not found in cache", callback->ip);
        ngx_mail_throttle_whitelist_lookup_ip(callback);
    }
    else {
        ngx_log_error (NGX_LOG_ERR, log, 0,
            "cache failure trying to see if %V should be whitelisted", callback->ip);
        ngx_mail_throttle_ip(*callback->ip, callback);
    }
}

static ngx_str_t ngx_mail_throttle_ip_ttl_txt (
    ngx_mail_throttle_srv_conf_t * tscf,
    ngx_uint_t protocol
)
{
    ngx_str_t ip_ttl_txt;

    switch (protocol) {
        case NGX_MAIL_POP3_PROTOCOL:
            ip_ttl_txt = tscf->mail_login_ip_pop3_ttl_text;
            break;
        case NGX_MAIL_IMAP_PROTOCOL:
            ip_ttl_txt = tscf->mail_login_ip_imap_ttl_text;
            break;
        default:
            ip_ttl_txt = tscf->mail_login_ip_ttl_text;
    }
    return ip_ttl_txt;
}

static void ngx_mail_throttle_ip_add
    (ngx_str_t *ip, throttle_callback_t *callback)
{
    ngx_pool_t     *pool    = callback->pool;
    ngx_log_t      *log     = callback->log;
    ngx_mail_session_t  *s  = callback->session;
    ngx_mail_throttle_srv_conf_t * tscf;
    mc_work_t       w;
    ngx_str_t       k, value;
    ngx_str_t      *key;
    ngx_str_t       ip_ttl_text;

    ngx_log_error (NGX_LOG_INFO, log, 0, "counter for %V not found, "
                        "create ip throttle counter", ip);

    w.ctx = callback;
    w.request_code = mcreq_add;
    w.response_code = mcres_unknown;
    w.on_success = ngx_mail_throttle_ip_add_success_handler;
    w.on_failure = ngx_mail_throttle_ip_add_failure_handler;

    /* use ttl for discrete time sampling of ip login hits */
    tscf = ngx_mail_get_module_srv_conf(s, ngx_mail_throttle_module);
    ip_ttl_text = ngx_mail_throttle_ip_ttl_txt(tscf, s->protocol);
    k = ngx_mail_throttle_get_ip_throttle_key(pool, log, *ip, s->protocol);

    if (k.len == 0) {
        ngx_log_error (NGX_LOG_ERR, log, 0,
               "allowing ip %V login because of internal error "
               "in ip throttle control (generate key for add)", ip);
        callback->on_allow(callback);
        return;
    }

    ngx_log_debug3 (NGX_LOG_DEBUG_MAIL, log, 0,
        "ngx_mail_throttle_ip_add: protocol=%s, ip_ttl_text=%V, k=%V",
        ngx_encode_protocol(s->protocol, 'l'), &ip_ttl_text, &k);


    key = ngx_pstrcpy (pool, &k);
    if (key == NULL) {
        ngx_log_error (NGX_LOG_ERR, log, 0,
               "allowing ip %V login because of internal error "
               "in ip throttle control (deep copy key for add)", ip);
    }

    ngx_str_set(&value, "1");

    callback->value = ngx_pstrcpy (pool, &value);
    if (key == NULL) {
        ngx_log_error (NGX_LOG_ERR, log, 0,
               "allowing ip %V login because of internal error "
               "in ip throttle control (deep copy key for add)", ip);
    }
    callback->key = key;
    callback->ip = ip;
    callback->ttl = &ip_ttl_text;

    ngx_memcache_post_with_ttl(&w, *key, value, ip_ttl_text,/* pool */ NULL, log);
}

static void ngx_mail_throttle_ip_add_success_handler(mc_work_t *w)
{
    throttle_callback_t *callback = w->ctx;
    ngx_log_t           *log = callback->log;

    /* counter addition succeeded */
    ngx_log_error (NGX_LOG_INFO, log, 0,
        "ip throttle:%V counter created and access allowed", callback->ip);
    /* TODO handle extreme case where ip_limit is 0 or 1 */
    callback->on_allow(callback);
}

/* memcache error handler (connection error or memory allocation error) */
static void ngx_mail_throttle_ip_add_failure_handler (mc_work_t *w)
{
    throttle_callback_t   *callback = w->ctx;
    ngx_log_t             *log = callback->log;

    if (w->response_code == mcres_failure_normal) {
        /* Counter creation failed because of getting "NOT_STORED". This could
         * occur when more than one processes try to login and post "incr"
         * and all get "NOT_FOUND", and then try to add new counter. One of
         * them will get "STORED" and others will reach here. In some other
         * extreme cases, such as the ttl is very short, or some mis-handling
         * of memcache, this case may also happen. Considering the little
         * probability and the endurable inaccuracy, just ignore it.
         */
        ngx_log_error (NGX_LOG_NOTICE, log, 0,

            "allowing ip %V login because unable to create the "
            "ip counter", callback->ip);
        callback->on_allow(callback);

    } else if (w->response_code == mcres_failure_again) {
        mc_work_t nw;
        nw.ctx = callback;
        nw.request_code = mcreq_add;
        nw.response_code = mcres_unknown;
        nw.on_success = ngx_mail_throttle_ip_add_success_handler;
        nw.on_failure = ngx_mail_throttle_ip_add_failure_handler;
        ngx_log_error (NGX_LOG_NOTICE, log, 0,
                "retry to check ip throttle:[%V]", callback->ip);
        ngx_memcache_post_with_ttl(&nw, *callback->key, *callback->value,
                *callback->ttl, /* pool */ NULL, callback->log);
    } else { /* mcres_failure_unavailable */
        ngx_log_error (NGX_LOG_ERR, log, 0,
                "throttle allowing access from ip %V because "
                "error occurs in memcache module when try to "
                "create counter", callback->ip);
        callback->on_allow(callback);
    }
}

/* check whether the client user name should be allowed to proceed, or whether
   the connection should be throttled
 */
void ngx_mail_throttle_user (ngx_str_t user, throttle_callback_t *callback)
{
    ngx_pool_t          *pool;
    ngx_log_t           *log;
    ngx_connection_t    *c;
    ngx_str_t           *cusr;
    ngx_mail_session_t  *s;
    mc_work_t            w;
    ngx_str_t            proxyip;
    ngx_str_t           *dummy_value;

    pool = callback->pool;
    log = callback->log;
    c = callback->connection;
    s = callback->session;

    ngx_log_debug1 (NGX_LOG_DEBUG_MAIL, log, 0,
        "user throttle: lookup alias, user:%V", &user);

    /* save a copy of the user name */
    cusr = ngx_pstrcpy(pool, &user);
    if (cusr == NULL) {
        ngx_log_error (NGX_LOG_ERR, log, 0,
                "allowing user %V login because of internal error "
                "in user throttle control (deep copy user for incr)", &user);
        callback->on_allow(callback);
        return;
    }

    if (s->vlogin) {
        /* user alias has already been looked up */
        ngx_log_debug1 (NGX_LOG_DEBUG_MAIL, log, 0,
            "user throttle: skip alias lookup, user:%V", &user);
        ngx_mail_throttle_quser(cusr, callback);
        return;
    }

    w.ctx = callback;
    w.request_code = mcreq_get;
    w.response_code = mcres_unknown;
    w.on_success = ngx_mail_throttle_user_success_handler;
    w.on_failure = ngx_mail_throttle_user_failure_handler;

    /* GSSAPI workaround: don't lookup aliases for GSSAPI */
    if (s->auth_method == NGX_MAIL_AUTH_GSSAPI) {
        ngx_log_error(NGX_LOG_INFO, log, 0,
            "not looking up cached aliases for auth=gssapi");
        ngx_mail_throttle_quser(cusr, callback);
        return;
    }

    /* first stringify the proxy-ip address */
    proxyip = ngx_mail_get_socket_local_addr_str (pool, c->fd);

    s->key_alias = ngx_zm_lookup_get_mail_alias_key(
            pool,
            log,
            *cusr,
            proxyip
        );

    if (s->key_alias.len == 0) {
        ngx_log_error (NGX_LOG_ERR, log, 0,
                "allowing user %V login because of internal error "
                "in user throttle control (create alias key)", &user);
        callback->on_allow(callback);
        return;
    }

    dummy_value = ngx_palloc (pool, sizeof (ngx_str_t));

    ngx_str_null (dummy_value);

    callback->key = &s->key_alias;
    callback->value = dummy_value;
    callback->user = cusr;

    ngx_memcache_post(&w, s->key_alias, *dummy_value,/* pool */ NULL, log);
}

/* callback to replace login user name with an alias, if any */
static void ngx_mail_throttle_user_success_handler (mc_work_t *w)
{
    throttle_callback_t     *callback = w->ctx;
    ngx_mail_session_t      *s = callback->session;
    ngx_str_t                login; //full qualified name

    /* deep copy w->payload onto s->login (pool is callback->pool) */
    login.data = ngx_pstrdup (callback->pool, &w->payload);
    if (login.data != NULL)
    {
        login.len = w->payload.len;
        s->vlogin = 2; // lookup alias and found
        s->qlogin = login;
        ngx_log_error (NGX_LOG_INFO, callback->log, 0,
            "user throttle: alias %V replaced by %V",
            callback->user, &s->login);
        ngx_mail_throttle_quser (&s->login, callback);
    } else {
        ngx_mail_throttle_quser (callback->user, callback);
    }
}

static void ngx_mail_throttle_user_failure_handler (mc_work_t *w)
{
    throttle_callback_t  *callback = w->ctx;
    ngx_str_t            *user = callback->user;
    ngx_mail_session_t   *s = callback->session;
    ngx_log_t            *log = callback->log;

    if (w->response_code == mcres_failure_normal) {
        //NOT_FOUND
        ngx_log_error(NGX_LOG_INFO, log, 0,
            "user throttle: no alias for user:%V",
            user);
        s->vlogin = 1;  /* avoid duplicate lookups for alias */
        s->qlogin = s->login;
        ngx_mail_throttle_quser (callback->user, callback);

    } else if(w->response_code == mcres_failure_again) {
        mc_work_t nw;
        nw.ctx = callback;
        nw.request_code = mcreq_get;
        nw.response_code = mcres_unknown;
        nw.on_success = ngx_mail_throttle_user_success_handler;
        nw.on_failure = ngx_mail_throttle_user_failure_handler;
        ngx_log_error (NGX_LOG_NOTICE, callback->log, 0,
                "retry to lookup alias %V before user throttle", callback->user);
        ngx_memcache_post(&nw, *callback->key, *callback->value,
                            /* pool */ NULL, log);

    } else if(w->response_code == mcres_failure_input) {
        ngx_log_error (NGX_LOG_ERR, log, 0,
                       "throttle deny since the user name %V is invalid",
                       callback->user);
        callback->on_deny(callback);
    } else { /* mcres_failure_unavailable */
        ngx_log_error (NGX_LOG_ERR, log, 0,
                "throttle allowing access from user %V because "
                "memcache service is unavailable when try to "
                "perform alias lookup", callback->user);
        callback->on_allow(callback);
    }
}

/* same as ngx_mail_throttle_user, but works on a fully qualified user name */
static void ngx_mail_throttle_quser (ngx_str_t * quser, throttle_callback_t *callback)
{
    ngx_log_t           *log;
    ngx_pool_t          *pool;
    mc_work_t            w;
    ngx_str_t            k;
    ngx_str_t           *value, *key;
    ngx_flag_t           check_only;

    pool = callback->pool;
    log = callback->log;
    check_only = callback->check_only;

    k = ngx_mail_throttle_get_user_throttle_key(pool, log, *quser);
    if (k.len == 0) {
        ngx_log_error (NGX_LOG_ERR, log, 0,
            "allowing user %V login because of internal error "
            "in user throttle control (generate key for get)", quser);
        callback->on_allow(callback);
        return;
    }

    key = ngx_pstrcpy (pool, &k);
    if (key == NULL) {
        ngx_log_error (NGX_LOG_ERR, log, 0,
            "allowing user %V login because of internal error "
            "in user throttle control (deep copy check user key)", quser);
        callback->on_allow(callback);
    }

    if (check_only == 0)
    {   // try to increment the counter for this user
        ngx_log_error (NGX_LOG_INFO, log, 0, "check user throttle:%V", quser);
        w.ctx = callback;
        w.request_code = mcreq_incr;
        w.response_code = mcres_unknown;
        w.on_success = ngx_mail_throttle_quser_success_handler;
        w.on_failure = ngx_mail_throttle_quser_failure_handler;

        value = ngx_palloc (pool, sizeof(ngx_str_t));
        if (value == NULL) {
            ngx_log_error (NGX_LOG_ERR, log, 0,
                    "allowing user %V login because of internal error"
                    "in ip throttle control (alloc mem for incr value)", quser);
            callback->on_allow(callback);
            return;
        }

        ngx_str_set(value, "1");
    }
    else
    {   // just check the counter
        ngx_log_error (NGX_LOG_INFO, log, 0, "check user throttle:%V, check only", quser);
        w.ctx = callback;
        w.request_code = mcreq_get;
        w.response_code = mcres_unknown;
        w.on_success = ngx_mail_throttle_quser_success_handler;
        w.on_failure = ngx_mail_throttle_quser_failure_handler;

        value = ngx_palloc (pool, sizeof(ngx_str_t));
        if (value == NULL) {
            ngx_log_error (NGX_LOG_ERR, log, 0,
                    "allowing ip %V login because of internal error"
                    "in user throttle control (alloc mem for get value)", quser);
            callback->on_allow(callback);
            return;
        }

        ngx_str_null (value);
    }

    callback->key = key;
    callback->value = value;
    callback->user = quser;

    ngx_memcache_post(&w, *key, *value,/* pool */ NULL, log);
}

static void ngx_mail_throttle_quser_success_handler (mc_work_t *w)
{
    throttle_callback_t     *callback = w->ctx;
    ngx_mail_session_t      *s = callback->session;
    ngx_log_t               *log = callback->log;
    ngx_mail_throttle_srv_conf_t * tscf;
    size_t                   hits;
    ngx_str_t                counter;

    /* increment succeeded / get succeeded */
    counter.data = ngx_pstrdup(callback->pool, &w->payload);

    if (counter.data == NULL) { /* enomem */
        counter = throttle_zero;
    } else {
        counter.len = w->payload.len;
    }

    /* check if the limit has exceeded */
    ngx_log_debug2 (NGX_LOG_DEBUG_MAIL, log, 0,
        "user throttle:%V is %V", callback->user, &counter);

    hits = ngx_atoi (counter.data, counter.len);

    tscf = ngx_mail_get_module_srv_conf (s, ngx_mail_throttle_module);
    if (tscf->mail_login_user_max == 0) {
        //should never reach here because unlimited case has been handled
        ngx_log_error (NGX_LOG_INFO, log, 0,
            "user throttle:%V allow [count:%d,limit:inf]",
            callback->user, hits);
        callback->on_allow(callback);
    } else if (hits <= tscf->mail_login_user_max) {
        ngx_log_error (NGX_LOG_INFO, log, 0,
            "user throttle:%V allow [count:%d,limit:%d]",
            callback->user, hits, tscf->mail_login_user_max);
        callback->on_allow(callback);
    } else {
        ngx_log_error (NGX_LOG_NOTICE, log, 0,
            "user throttle:%V deny [count:%d,limit:%d]",
            callback->user, hits, tscf->mail_login_user_max);
        callback->on_deny(callback);
    }
}

static void ngx_mail_throttle_quser_failure_handler (mc_work_t *w)
{
    throttle_callback_t *callback = w->ctx;
    ngx_log_t           *log = callback->log;
    ngx_flag_t           check_only = callback->check_only;

    if (w->response_code == mcres_failure_normal) {
        if (check_only) {
           ngx_log_error (NGX_LOG_INFO, log, 0,
                "user throttle:%V not found, allow due to check only",
                callback->user);
           callback->on_allow(callback);
       } else {
           ngx_log_debug1(NGX_LOG_DEBUG_MAIL, log, 0,
                "user throttle:%V add counter", callback->user);
           ngx_mail_throttle_user_add(callback->user, callback);
       }

    } else if (w->response_code == mcres_failure_again) {
        mc_work_t nw;
        nw.ctx = callback;
        if (check_only) {
            nw.request_code = mcreq_get;
        } else {
            nw.request_code = mcreq_incr;
        }
        nw.response_code = mcres_unknown;
        nw.on_success = ngx_mail_throttle_quser_success_handler;
        nw.on_failure = ngx_mail_throttle_quser_failure_handler;
        ngx_log_error (NGX_LOG_NOTICE, log, 0,
                "retry to check user throttle:%V", callback->user);
        ngx_memcache_post(&nw, *callback->key, *callback->value,
                            /* pool */ NULL, log);
        } else if(w->response_code == mcres_failure_input) {
            ngx_log_error (NGX_LOG_ERR, log, 0,
                       "throttle deny since the user name %V is invalid",
                       callback->user);
            callback->on_deny(callback);
        } else { /* mcres_failure_unavailable */
            if (check_only) {
                ngx_log_error (NGX_LOG_ERR, log, 0,
                    "throttle allowing access from user %V because "
                    "memcache service is unavailable when try to "
                    "get user counter", callback->user);
            } else {
                ngx_log_error (NGX_LOG_ERR, log, 0,
                    "throttle allowing access from user %V because "
                    "memcache service is unavailable when try to "
                    "increment user counter", callback->user);
            }
        callback->on_allow(callback);
    }
}

/* add a throttle counter for a user, here user might be an alias or a fqn */
static void ngx_mail_throttle_user_add
    (ngx_str_t *user, throttle_callback_t *callback)
{
    ngx_pool_t             *pool    = callback->pool;
    ngx_log_t              *log     = callback->log;
    ngx_mail_session_t     *s       = callback->session;
    ngx_mail_throttle_srv_conf_t *tscf;
    mc_work_t               w;
    ngx_str_t               k;
    ngx_str_t              *value, *key;

    ngx_log_error (NGX_LOG_INFO, log, 0, "create a throttle counter for user %V", user);
    w.ctx = callback;
    w.request_code = mcreq_add;
    w.response_code = mcres_unknown;
    w.on_success = ngx_mail_throttle_user_add_success_handler;
    w.on_failure = ngx_mail_throttle_user_add_failure_handler;

    k = ngx_mail_throttle_get_user_throttle_key(pool, log, *user);
    if (k.len == 0) {
        ngx_log_error (NGX_LOG_ERR, log, 0,
            "allowing user %V login because of internal error "
            "in user throttle control (generate key for add)", user);
        callback->on_allow(callback);
        return;
    }

    key = ngx_pstrcpy (pool, &k);
    if (key == NULL) {
        ngx_log_error (NGX_LOG_ERR, log, 0,
            "allowing user %V login because of internal error "
            "in user throttle control (deep copy key for add)", user);
        callback->on_allow(callback);
        return;
    }

    tscf = ngx_mail_get_module_srv_conf (s, ngx_mail_throttle_module);

    value = ngx_palloc (pool, sizeof(ngx_str_t));
    if (value == NULL) {
       ngx_log_error (NGX_LOG_ERR, log, 0,
               "allowing user %V login because of internal error"
               "in user throttle control (alloc mem for add value)", user);
       callback->on_allow(callback);
       return;
    }

    ngx_str_set(value, "1");

    callback->key = key;
    callback->value = value;
    callback->user = user;
    callback->ttl = &tscf->mail_login_user_ttl_text;

    ngx_memcache_post_with_ttl(&w, *key, *value, tscf->mail_login_user_ttl_text,
            /* pool */ NULL, log);
    return;
}

static void ngx_mail_throttle_user_add_success_handler(mc_work_t *w)
{
    throttle_callback_t *callback = w->ctx;
    ngx_log_t           *log = callback->log;

    /* counter addition succeeded */
    ngx_log_error (NGX_LOG_INFO, log, 0,
        "throttle allowing access from user %V, counter created",
        callback->user);
    callback->on_allow(callback);
}

/* memcache error handler (connection error or memory allocation error) */
static void ngx_mail_throttle_user_add_failure_handler (mc_work_t *w)
{
    throttle_callback_t  *callback = w->ctx;
    ngx_log_t            *log = callback->log;

    if (w->response_code == mcres_failure_normal) {
        /* Counter creation failed because of getting "NOT_STORED". This could
         * occur when more than one processes try to login and post "incr"
         * and all get "NOT_FOUND", and then try to add new counter. One of
         * them will get "STORED" and others will reach here. In some other
         * extreme cases, such as the ttl is very short, or some mis-handling
         * of memcache, this case may also happen. Considering the little
         * probability and the endurable inaccuracy, just ignore it.
         */
        ngx_log_error (NGX_LOG_NOTICE, log, 0,
            "allowing user %V login because unable to create the "
            "user counter", callback->user);
        callback->on_allow(callback);

    } else if (w->response_code == mcres_failure_again) {
        mc_work_t nw;
        nw.ctx = callback;
        nw.request_code = mcreq_add;
        nw.response_code = mcres_unknown;
        nw.on_success = ngx_mail_throttle_user_add_success_handler;
        nw.on_failure = ngx_mail_throttle_user_add_failure_handler;
        ngx_log_error (NGX_LOG_NOTICE, log, 0,
                "retry to check user throttle:%V", callback->user);
        ngx_memcache_post_with_ttl(&nw, *callback->key, *callback->value,
                            *callback->ttl, /* pool */ NULL, log);
    } else {
        ngx_log_error (NGX_LOG_ERR, log, 0,
            "throttle allowing access from ip %V because "
            "memcache service is unavailable when try to "
            "create user counter", callback->user);
        callback->on_allow(callback);
    }
}

static ngx_str_t
ngx_mail_throttle_get_user_throttle_key (
    ngx_pool_t      *pool,
    ngx_log_t       *log,
    ngx_str_t        user
)
{
    ngx_str_t       k;
    u_char         *p;
    size_t          l;
    uintptr_t       escape;

    escape = 2 * ngx_escape_uri(NULL, user.data, user.len,
            NGX_ESCAPE_MEMCACHED);

    l = sizeof("throttle:") - 1 +
        sizeof("user=") - 1 +
        user.len + escape;

    k.data = ngx_palloc(pool, l);
    if (k.data == NULL)
    {
        k.len = 0;
        return k;
    }

    p = k.data;
    p = ngx_cpymem(p, "throttle:", sizeof("throttle:") - 1);
    p = ngx_cpymem(p, "user=", sizeof("user=") - 1);

    if (escape == 0) {
        p = ngx_cpymem(p, user.data, user.len);
    } else {
        p = (u_char *)ngx_escape_uri(p, user.data, user.len,
                NGX_ESCAPE_MEMCACHED);
    }

    k.len = p - k.data;

    return k;
}

static char *
ngx_encode_protocol (
    ngx_uint_t protocol,
    char eptype			/* s=short, l (or anything else)=long */
)
{
    switch (protocol) {
        case NGX_MAIL_POP3_PROTOCOL:
            return eptype == 's' ? "p" : "pop3";
        case NGX_MAIL_IMAP_PROTOCOL:
            return eptype == 's' ? "i" : "imap";
        case NGX_MAIL_SMTP_PROTOCOL:
            return eptype == 's' ? "s" : "smtp";
        default:
            return eptype = 's' ? "u" : "unknown";
    }
}

static ngx_str_t
ngx_mail_throttle_get_ip_throttle_key (
    ngx_pool_t      *pool,
    ngx_log_t       *log,
    ngx_str_t        ip,
    ngx_uint_t	     protocol
)
{
    ngx_str_t   k;
    size_t      l;
    u_char     *p;

    l = sizeof("throttle:") - 1 +
        sizeof("proto=") - 1 +
        1 +
        sizeof(",ip=") - 1 +
        ip.len;

    k.data = ngx_palloc(pool, l);
    if (k.data == NULL)
    {
        k.len = 0;
        return k;
    }

    p = k.data;
    p = ngx_cpymem(p, "throttle:", sizeof("throttle:") - 1);
    p = ngx_cpymem(p, "proto=", sizeof("proto=") - 1);
    p = ngx_cpymem(p, ngx_encode_protocol(protocol, 's'), 1);
    p = ngx_cpymem(p, ",ip=", sizeof(",ip=") - 1);
    p = ngx_cpymem(p, ip.data, ip.len);

    k.len = p - k.data;

    return k;
}

static ngx_str_t
ngx_mail_throttle_get_ip_whitelist_key (
    ngx_pool_t      *pool,
    ngx_log_t       *log,
    ngx_str_t        ip
)
{
    ngx_str_t   k;
    size_t      l;
    u_char     *p;

    l = sizeof("whitelist:") - 1 +
        sizeof("ip=") - 1 +
        ip.len;

    k.data = ngx_palloc(pool, l);
    if (k.data == NULL)
    {
        k.len = 0;
        return k;
    }

    p = k.data;
    p = ngx_cpymem(p, "whitelist:", sizeof("whitelist:") - 1);
    p = ngx_cpymem(p, "ip=", sizeof("ip=") - 1);
    p = ngx_cpymem(p, ip.data, ip.len);

    k.len = p - k.data;

    return k;
}

