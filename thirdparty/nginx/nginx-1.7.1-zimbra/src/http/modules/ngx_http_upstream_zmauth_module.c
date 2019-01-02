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

#include <ngx_config.h>
#include <ngx_core.h>
#include <ngx_http.h>
#include <ngx_zm_lookup.h>
#include <ngx_http_upstream_zmauth_module.h>
#include <ctype.h>

static char *ngx_http_upstream_fair_set_shm_size(ngx_conf_t *cf,
                                                 ngx_command_t *cmd, void *conf);
static char * ngx_http_upstream_zmauth(ngx_conf_t *cf, ngx_command_t *cmd,
        void *conf);
static char * ngx_http_upstream_zmauth_admin(ngx_conf_t *cf, ngx_command_t *cmd,
        void *conf);

static char * ngx_http_upstream_zmauth_zx(ngx_conf_t *cf, ngx_command_t *cmd,
        void *conf);

static void *ngx_http_upstream_zmauth_create_srv_conf(ngx_conf_t *cf);
static char *ngx_http_upstream_zmauth_merge_srv_conf(ngx_conf_t *cf,
        void *parent, void *child);

static ngx_int_t ngx_http_upstream_init_zmauth_peer(ngx_http_request_t *r,
        ngx_http_upstream_srv_conf_t *us);
static ngx_int_t ngx_http_upstream_init_admin_zmauth_peer(ngx_http_request_t *r,
        ngx_http_upstream_srv_conf_t *us);
static ngx_int_t ngx_http_upstream_init_zx_zmauth_peer(ngx_http_request_t *r,
        ngx_http_upstream_srv_conf_t *us);
static ngx_int_t ngx_http_upstream_do_init_zmauth_peer(ngx_http_request_t *r,
        ngx_http_upstream_srv_conf_t *us, ngx_http_zmauth_t type);
static ngx_int_t ngx_http_upstream_get_zmauth_peer(ngx_peer_connection_t *pc,
        void *data);
static void ngx_http_upstream_free_zmauth_peer(ngx_peer_connection_t *pc,
        void *data, ngx_uint_t state);
static void zmauth_lookup_result_handler(ngx_zm_lookup_work_t *work);
static void ngx_http_upstream_zmauth_cleanup(void *data);

static ngx_uint_t zmauth_get_current_peer(
        ngx_http_upstream_zmauth_peer_data_t *zmp);
static inline void zmauth_set_peer(ngx_peer_connection_t *pc,
        ngx_http_upstream_zmauth_peer_data_t *zmp);

static ngx_flag_t zmauth_check_rest(ngx_http_request_t *r, void **extra);
static ngx_flag_t zmauth_check_activesync(ngx_http_request_t *r, void **extra);
static ngx_flag_t zmauth_check_ews(ngx_http_request_t *r, void **extra);
static ngx_flag_t zmauth_check_caldav(ngx_http_request_t *r, void **extra);
static ngx_flag_t zmauth_check_authtoken(ngx_http_request_t *r, ngx_str_t *field, void **extra);
static ngx_flag_t zmauth_check_jwttoken(ngx_http_request_t *r, ngx_str_t *field, void **extra);
static ngx_flag_t zmauth_check_admin_authtoken(ngx_http_request_t *r, ngx_str_t *field,
        void **extra);
static zmroutetype_t zmauth_check_uri(ngx_http_request_t *r, void **extra);
static zmroutetype_t zmauth_check_admin_uri(ngx_http_request_t *r, void **extra);
static ngx_flag_t zmauth_find_arg(/* const */ngx_str_t *args, /* const */
ngx_str_t *arg, ngx_str_t *val);

#ifdef unused
static ngx_flag_t ngx_http_upstream_zmserver_from_cookie
(ngx_log_t *log, ngx_pool_t *pool, ngx_table_elt_t *cookie, ngx_addr_t *peer);
#endif

static void zmauth_translate_activesync_ews_usr(ngx_pool_t *pool, ngx_str_t *src,
        ngx_str_t *tgt);
static ngx_flag_t ngx_field_from_zmauthtoken(ngx_log_t *log, ngx_pool_t *pool,
        ngx_str_t *authtoken, ngx_str_t *field, ngx_str_t *value);
static ngx_flag_t ngx_claimdata_from_jwttoken(ngx_log_t *log, ngx_pool_t *pool,
        ngx_str_t *authtoken, ngx_str_t *field, ngx_str_t *value);
static ngx_flag_t ngx_get_authheader_bearer(ngx_log_t *log, ngx_pool_t *pool,
        ngx_http_headers_in_t *headers_in, ngx_str_t *value);
static ngx_flag_t ngx_claimdata_from_payload(ngx_log_t *log, ngx_pool_t *pool,
        ngx_str_t *payload, ngx_str_t *value);
static ngx_flag_t ngx_get_cookie_value(ngx_log_t *log,
        ngx_table_elt_t **cookies, ngx_uint_t ncookies, ngx_str_t *name,
        ngx_str_t *value);
static ngx_flag_t ngx_get_query_string_arg(ngx_log_t *log, ngx_str_t *args,
        ngx_str_t *name, ngx_str_t *value);


static ngx_str_t NGX_ZMAUTHTOKEN_ID = ngx_string("id");
static ngx_str_t NGX_ZMAUTHTOKEN_VER = ngx_string("version");
static ngx_str_t NGX_ZMAUTHTOKEN = ngx_string("ZM_AUTH_TOKEN");
static ngx_str_t NGX_ZMAUTHTOKEN_ADMIN = ngx_string("ZM_ADMIN_AUTH_TOKEN");
static ngx_str_t NGX_ZAUTHTOKEN = ngx_string("zauthtoken");
static ngx_str_t NGX_ACCESS_DENIED_ERRMSG = ngx_string("is not allowed on this domain");

static ngx_str_t NGX_ZMJWT_CLAIM_ID = ngx_string("sub");
static ngx_str_t NGX_ZJWT_QUERY = ngx_string("zjwt");

static ngx_command_t ngx_http_upstream_zmauth_commands[] =
{
    { ngx_string("upstream_fair_shm_size"),
        NGX_HTTP_MAIN_CONF|NGX_CONF_TAKE1,
        ngx_http_upstream_fair_set_shm_size,
        0,
        0,
        NULL },

    { ngx_string("zmauth"),
      NGX_HTTP_UPS_CONF|NGX_CONF_NOARGS,
      ngx_http_upstream_zmauth,
      0,
      0,
      NULL },

    { ngx_string("zmauth_admin"),
      NGX_HTTP_UPS_CONF|NGX_CONF_NOARGS,
      ngx_http_upstream_zmauth_admin,
      0,
      0,
      NULL },

    { ngx_string("zmauth_zx"),
      NGX_HTTP_UPS_CONF|NGX_CONF_NOARGS,
      ngx_http_upstream_zmauth_zx,
      0,
      0,
      NULL },

    ngx_null_command
};

static ngx_http_module_t ngx_http_upstream_zmauth_module_ctx = {
        NULL,                                       /* preconfiguration */
        NULL,                                       /* postconfiguration */
        NULL,                                       /* create main configuration */
        NULL,                                       /* init main configuration */
        ngx_http_upstream_zmauth_create_srv_conf,   /* create server config */
        ngx_http_upstream_zmauth_merge_srv_conf,    /* merge server config */
        NULL,                                       /* create location configuration */
        NULL                                        /* merge location configuration */
};

ngx_module_t ngx_http_upstream_zmauth_module = {
        NGX_MODULE_V1,
        &ngx_http_upstream_zmauth_module_ctx,
        ngx_http_upstream_zmauth_commands,
        NGX_HTTP_MODULE,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NGX_MODULE_V1_PADDING
};

static char *
ngx_http_upstream_fair_set_shm_size(ngx_conf_t *cf, ngx_command_t *cmd, void *conf)
{
    ssize_t                         new_shm_size;
    ngx_str_t                      *value;

    value = cf->args->elts;

    new_shm_size = ngx_parse_size(&value[1]);

    if (new_shm_size == NGX_ERROR) {
        ngx_log_error(NGX_LOG_EMERG, cf->log, 0, "Invalid memory area size `%V'", &value[1]);
        return NGX_CONF_ERROR;
    }

    new_shm_size = ngx_align(new_shm_size, ngx_pagesize);

    if (new_shm_size < 8 * (ssize_t) ngx_pagesize) {
        ngx_log_error(NGX_LOG_WARN, cf->log, 0, "The upstream_fair_shm_size value must be at least %udKiB", (8 * ngx_pagesize) >> 10);
        new_shm_size = 8 * ngx_pagesize;
    }

    if (*shm_size && *shm_size != (ngx_uint_t) new_shm_size) {
        ngx_log_error(NGX_LOG_WARN, cf->log, 0, "Cannot change memory area size without restart, ignoring change");
    } else {
        *shm_size = new_shm_size;
    }
    ngx_log_error(NGX_LOG_NOTICE, cf->log, 0, "Using %udKiB of shared memory for upstream_fair", *shm_size >> 10);

    return NGX_CONF_OK;
}

/* handle the `zmauth' configuration directive in an upstream block
 */
static char *
ngx_http_upstream_zmauth(ngx_conf_t *cf, ngx_command_t *cmd, void *conf)
{
    ngx_http_upstream_srv_conf_t *uscf;

    uscf = ngx_http_conf_get_module_srv_conf(cf, ngx_http_upstream_module);
    uscf->peer.init_upstream = ngx_http_upstream_init_zmauth;

    uscf->flags = NGX_HTTP_UPSTREAM_CREATE | NGX_HTTP_UPSTREAM_MAX_FAILS
            | NGX_HTTP_UPSTREAM_FAIL_TIMEOUT | NGX_HTTP_UPSTREAM_DOWN | NGX_HTTP_UPSTREAM_VERSION;

    return NGX_CONF_OK;
}

static char *
ngx_http_upstream_zmauth_admin(ngx_conf_t *cf, ngx_command_t *cmd, void *conf)
{
    ngx_http_upstream_srv_conf_t *uscf;

    uscf = ngx_http_conf_get_module_srv_conf(cf, ngx_http_upstream_module);
    uscf->peer.init_upstream = ngx_http_upstream_init_admin_zmauth;

    uscf->flags = NGX_HTTP_UPSTREAM_CREATE | NGX_HTTP_UPSTREAM_MAX_FAILS
            | NGX_HTTP_UPSTREAM_FAIL_TIMEOUT | NGX_HTTP_UPSTREAM_DOWN | NGX_HTTP_UPSTREAM_VERSION;

    return NGX_CONF_OK;
}

static char *
ngx_http_upstream_zmauth_zx(ngx_conf_t *cf, ngx_command_t *cmd, void *conf)
{
    ngx_http_upstream_srv_conf_t *uscf;

    uscf = ngx_http_conf_get_module_srv_conf(cf, ngx_http_upstream_module);
    uscf->peer.init_upstream = ngx_http_upstream_init_zx_zmauth;

    uscf->flags = NGX_HTTP_UPSTREAM_CREATE | NGX_HTTP_UPSTREAM_MAX_FAILS
                  | NGX_HTTP_UPSTREAM_FAIL_TIMEOUT | NGX_HTTP_UPSTREAM_DOWN | NGX_HTTP_UPSTREAM_VERSION;

    return NGX_CONF_OK;
}

/* This is the 'init_upstream' routine -- called when the main upstream
 configuration is initialized -- at this point, all the component servers
 in the upstream block should already be known, so that data-structures
 can be initialized here
 */
ngx_int_t
ngx_http_upstream_init_zmauth(ngx_conf_t *cf, ngx_http_upstream_srv_conf_t *us)
{
    if (ngx_http_upstream_init_fair(cf, us) != NGX_OK) {
        return NGX_ERROR;
    }

    us->peer.init = ngx_http_upstream_init_zmauth_peer;
    return NGX_OK;
}

ngx_int_t
ngx_http_upstream_init_admin_zmauth(ngx_conf_t *cf, ngx_http_upstream_srv_conf_t *us)
{
    if (ngx_http_upstream_init_fair(cf, us) != NGX_OK) {
        return NGX_ERROR;
    }

    us->peer.init = ngx_http_upstream_init_admin_zmauth_peer;
    return NGX_OK;
}

ngx_int_t
ngx_http_upstream_init_zx_zmauth(ngx_conf_t *cf, ngx_http_upstream_srv_conf_t *us)
{
    if (ngx_http_upstream_init_fair(cf, us) != NGX_OK) {
        return NGX_ERROR;
    }

    us->peer.init = ngx_http_upstream_init_zx_zmauth_peer;
    return NGX_OK;
}

static ngx_int_t
ngx_http_upstream_init_zmauth_peer(ngx_http_request_t *r,
        ngx_http_upstream_srv_conf_t *us)
{
    return ngx_http_upstream_do_init_zmauth_peer(r, us, zmauth_web_client);
}

static ngx_int_t
ngx_http_upstream_init_admin_zmauth_peer(ngx_http_request_t *r,
        ngx_http_upstream_srv_conf_t *us)
{
    return ngx_http_upstream_do_init_zmauth_peer(r, us, zmauth_admin_console);
}

static ngx_int_t
ngx_http_upstream_init_zx_zmauth_peer(ngx_http_request_t *r,
                                         ngx_http_upstream_srv_conf_t *us)
{
    return ngx_http_upstream_do_init_zmauth_peer(r, us, zmauth_zx);
}

/* This function is called when an incoming http request needs to be routed to
 one of the peers inside the upstream block
 */
static ngx_int_t
ngx_http_upstream_do_init_zmauth_peer(ngx_http_request_t *r,
        ngx_http_upstream_srv_conf_t *us, ngx_http_zmauth_t type)
{
    ngx_http_upstream_zmauth_peer_data_t *zmp;
    struct sockaddr_in                   *sin;
    struct sockaddr_in6                  *sin6;
    int                                   i;
    u_char                               *p, *q;
    ngx_str_t                             usr, schema;
    ngx_http_upstream_zmauth_ctx_t       *ctx;
    ngx_pool_t                           *pool;
    void                                 *info;
    void								 *ver;
    ngx_zm_lookup_work_t                 *work;

    ngx_log_debug0 (NGX_LOG_DEBUG_ZIMBRA, r->connection->log, 0,
            "zmauth: lookup route for web proxy");

    zmp = ngx_pcalloc(r->pool, sizeof(ngx_http_upstream_zmauth_peer_data_t));

    if (zmp == NULL) {
        return NGX_ERROR;
    }

    r->upstream->peer.data = &zmp->fp;
    if (ngx_http_upstream_init_fair_peer(r, us) != NGX_OK) {
        ngx_log_debug0 (NGX_LOG_DEBUG_HTTP, r->connection->log, 0,
                "zmauth: cannot initialize fair fallback");
        return NGX_ERROR;
    }

    r->upstream->peer.get = ngx_http_upstream_get_zmauth_peer;
    r->upstream->peer.free = ngx_http_upstream_free_zmauth_peer;
    zmp->get_fair_peer = ngx_http_upstream_get_fair_peer;

    /* initialize data for iphash for cases before AUTH TOKEN (prelogin) */
    zmp->family = r->connection->sockaddr->sa_family;
    if (zmp->family == AF_INET6) {
        sin6 = (struct sockaddr_in6 *) r->connection->sockaddr;
        p = (u_char *) &sin6->sin6_addr.s6_addr;
        for (i = 0; i < 16; i++) {
            zmp->addr[i] = p[i];
        }
        q = (u_char *) &sin6->sin6_port;
    } else {
        sin = (struct sockaddr_in *) r->connection->sockaddr;
        p = (u_char *) &sin->sin_addr.s_addr;
        for (i = 0; i < 4; i++) {
            zmp->addr[i] = p[i];
        }
        q = (u_char *) &sin->sin_port;
    }
    zmp->porth = q[0];
    zmp->portl = q[1];

    zmp->hash = 89;
    zmp->tries = 0;

    if (type == zmauth_web_client || type == zmauth_zx) {
        zmp->zmroutetype = zmauth_check_uri(r, &info);
        if (&zmp->fp && (zmp->zmroutetype == zmroutetype_authtoken) && zmauth_check_authtoken(r, &NGX_ZMAUTHTOKEN_VER, &ver)) {
        	zmp->fp.version = *((ngx_str_t*) ver);
        }
    } else if (type == zmauth_admin_console) {
        zmp->zmroutetype = zmauth_check_admin_uri(r, &info);
        if (&zmp->fp && (zmp->zmroutetype == zmroutetype_authtoken) && zmauth_check_admin_authtoken(r, &NGX_ZMAUTHTOKEN_VER, &ver)) {
            zmp->fp.version = *((ngx_str_t*) ver);
        }
    } else {
        zmp->zmroutetype = zmroutetype_fallback;
    }

    if (zmp->zmroutetype != zmroutetype_fallback) {
        usr = *((ngx_str_t*) info);

        ngx_log_debug0 (NGX_LOG_DEBUG_HTTP, r->connection->log, 0,
                "zmauth: route lookup required to proxy request");

        pool = ngx_create_pool(2048, r->connection->log);
        if (pool == NULL) {
            return NGX_ERROR;
        }
        ctx = ngx_pcalloc(pool, sizeof(ngx_http_upstream_zmauth_ctx_t));
        if (ctx == NULL) {
            ngx_destroy_pool(pool);
            return NGX_ERROR;
        }

        ngx_http_set_ctx(r, ctx, ngx_http_upstream_zmauth_module);
        ctx->pool = pool;
        ctx->zmp = zmp;

        //prepare cleanup
        ngx_http_cleanup_t * cln = ngx_http_cleanup_add(r, 0);
        cln->handler = ngx_http_upstream_zmauth_cleanup;
        cln->data = r;
        work = ngx_pcalloc(pool, sizeof(ngx_zm_lookup_work_t));
        if(work == NULL) {
            ngx_destroy_pool(pool);
            return NGX_ERROR;
        }
        work->pool = pool;
        work->log = r->connection->log;
        work->connection = r->connection;
        work->data = r;
        work->username = usr;
        if (r->headers_in.host != NULL) {
            work->virtual_host = r->headers_in.host->value;
        }
        work->alias_check_stat = ZM_ALIAS_NOT_CHECKED;
        work->on_success = zmauth_lookup_result_handler;
        work->on_failure = zmauth_lookup_result_handler;
        schema = r->upstream->schema;
        if (schema.len == sizeof("http://") - 1
                && ngx_strncmp(schema.data, (u_char *)"http://", sizeof("http://") - 1) == 0) {
            work->protocol = ZM_PROTO_HTTP;
        } else if (schema.len == sizeof("https://") - 1
                && ngx_strncmp(schema.data, (u_char *) "https://", sizeof("https://") - 1) == 0) {
            work->protocol = ZM_PROTO_HTTPS;
        }

        if (zmp->zmroutetype == zmroutetype_authtoken || zmp->zmroutetype == zmroutetype_jwttoken) {
            work->auth_method = ZM_AUTHMETH_ZIMBRAID;
        } else {
            work->auth_method = ZM_AUTHMETH_USERNAME;
        }

        work->type = type;

        ctx->work = work;
        ctx->connect = us->connect;
        ngx_zm_lookup(work);

        return NGX_AGAIN; // return NGX_AGAIN to indicate this is an async peer init
    }
    /* otherwise, routetype is fallback, then IPHASH will be used during getting peer */

    return NGX_OK;
}

/* This method is invoked in order to fill in the sockaddr, socklen, and name
 parameters of the peer connection data-structure (ngx_peer_connection_t)
 */
static ngx_int_t
ngx_http_upstream_get_zmauth_peer(ngx_peer_connection_t *pc,
        void *data) {
    ngx_http_upstream_zmauth_peer_data_t *zmp = data;
    ngx_http_upstream_fair_peer_t *peer;
    time_t now;
    uintptr_t m;
    ngx_uint_t i, n, p, hash, len;

    ngx_log_debug1 (NGX_LOG_DEBUG_HTTP, pc->log, 0,
            "zmauth: prepare upstream connection, try: %d",
            pc->tries);

    now = ngx_time();

    if (zmp->zmroutetype != zmroutetype_fallback) {
		ngx_log_debug1 (NGX_LOG_DEBUG_HTTP, pc->log, 0,
		            "zmauth: version in zm_auth_token: %V", &zmp->fp.version);
        zmp->fp.current = zmauth_get_current_peer(zmp);
        if (zmp->fp.current != NGX_INVALID_ARRAY_INDEX) {
            ngx_log_debug1 (NGX_LOG_DEBUG_HTTP, pc->log, 0,
                    "zmauth: upstream server %d is returned by zmlookup", zmp->fp.current);

            peer = &zmp->fp.peers->peer[zmp->fp.current];
            if (!peer->down) {

                if (peer->max_fails == 0 || peer->shared->fails < peer->max_fails) {
                    zmauth_set_peer(pc, zmp);
                    return NGX_OK;
                }

                if (now - peer->accessed > peer->fail_timeout) {
                    peer->shared->fails = 0;
                    zmauth_set_peer(pc, zmp);
                    return NGX_OK;
                }
            }

            zmp->fp.current = NGX_INVALID_ARRAY_INDEX;
            return NGX_BUSY;

        } else {
            ngx_log_debug1 (NGX_LOG_DEBUG_HTTP, pc->log, 0,
                    "zmauth: upstream server %V returned by zmlookup "
                    "is not defined in upstream block, fallback to IPHASH/Fair to pick an upstream from the upstream block",
                    &zmp->zmpeer.name);
            /* if the peer returned by zmlookup is not found in upstream block, just use it */
            /*
            if (zmp->tries > 0) { // have tried, won't try again
                return NGX_BUSY;
            }
            zmauth_set_peer(pc, zmp);
            zmp->tries++;
            return NGX_OK;
            */
        }
    }

    if (zmp->access_denied) {
        ngx_log_debug1 (NGX_LOG_DEBUG_HTTP, pc->log, 0,
                "zmauth: client IP %V", &NGX_ACCESS_DENIED_ERRMSG);
        zmp->access_denied = 0;
        return NGX_DECLINED;
    }

    /* check whether to use fair LB */
    if (zmp->tries > 20 || zmp->fp.peers->number == 1) {
        return zmp->get_fair_peer(pc, &zmp->fp);
    }

    pc->cached = 0;
    pc->connection = NULL;

    hash = zmp->hash;

    for (;;) {

        /* use all four octets of ipv4 address, plus two bytes of ipv4 port,
         for computation of ip-hash. this ensures better distribution
         */
        len = (zmp->family == AF_INET6) ? 16 : 4;
        for (i = 0; i < len; ++i) {
            hash = (hash * 113 + zmp->addr[i]) % 6271;
        }

        /*
         * since client IP PORT can change, client IP PORTS are not
         * used to generate HASH
         */
        //hash = (hash * 113 + zmp->porth) % 6271;
        //hash = (hash * 113 + zmp->portl) % 6271;

        zmp->hash = hash;

        p = hash % zmp->fp.peers->number;

        n = p / (8 * sizeof(uintptr_t));
        m = 1 << p % (8 * sizeof(uintptr_t));

        if (!(zmp->fp.tried[n] & m)) {

            ngx_log_debug4(NGX_LOG_DEBUG_HTTP, pc->log, 0,
                    "zmauth: get ip hash peer, peers = %ui hash = %ui selected peer index = %ui %04XA",
                    zmp->fp.peers->number, hash, p, m);

            peer = &zmp->fp.peers->peer[p];

            /* ngx_lock_mutex(iphp->fp.peers->mutex); */

            if (!peer->down) {
            	if (ngx_http_upstream_fair_peer_version_allowed(peer, &zmp->fp, pc->log) == 0) {
            		ngx_log_debug1(NGX_LOG_DEBUG_HTTP, pc->log, 0,
            		                    "zmauth: %V skipped because of version check, hash to a different upstream", &peer->name);
            		zmp->fp.tried[n] |= m;
            		pc->tries--;
            		if (++zmp->tries >= 20) {
            			return zmp->get_fair_peer(pc, &zmp->fp);
            		}
            		continue;
            	}

                if (peer->max_fails == 0 || peer->shared->fails < peer->max_fails) {
                    break;
                }

                if (now - peer->accessed > peer->fail_timeout) {
                    peer->shared->fails = 0;
                    break;
                }
            }

            zmp->fp.tried[n] |= m;

            /* ngx_unlock_mutex(iphp->fp.peers->mutex); */

            pc->tries--;
        }

        if (++zmp->tries >= 20) {
            return zmp->get_fair_peer(pc, &zmp->fp);
        }
    }

    zmp->fp.current = p;

    pc->sockaddr = peer->sockaddr;
    pc->socklen = peer->socklen;
    pc->name = &peer->name;

    ngx_log_debug1 (NGX_LOG_DEBUG_HTTP, pc->log, 0,
            "zmauth: %V elected by iphash", &peer->name);

    /* ngx_unlock_mutex(zmp->fp.peers->mutex); */

    zmp->fp.tried[n] |= m;
    zmp->hash = hash;

    return NGX_OK;
}

/* clean up zmauth ctx */
static void
ngx_http_upstream_zmauth_cleanup(void * data)
{
    ngx_http_request_t * r;
    ngx_http_upstream_zmauth_ctx_t * ctx;
    r = (ngx_http_request_t *)data;
    ctx = ngx_http_get_module_ctx(r, ngx_http_upstream_zmauth_module);
    if (ctx != NULL) {
        ngx_zm_lookup_finalize(ctx->work);
        ngx_destroy_pool(ctx->pool);
        ngx_http_set_ctx(r, NULL, ngx_http_upstream_zmauth_module);
    }
}

static void
zmauth_lookup_result_handler(ngx_zm_lookup_work_t * work) {
    ngx_http_request_t *r;
    ngx_http_upstream_zmauth_ctx_t *ctx;
    ngx_http_upstream_zmauth_peer_data_t *zmp;
    r = (ngx_http_request_t *) work->data;
    ctx = ngx_http_get_module_ctx(r, ngx_http_upstream_zmauth_module);
    zmp = ctx->zmp;

    if (work->result == ZM_LOOKUP_SUCCESS) {
        /* deep copy route from zmauth pool to r pool */
        zmp->zmpeer.name = *(ngx_pstrcpy(r->pool, &work->route->name));
        zmp->zmpeer.socklen = work->route->socklen;
        zmp->zmpeer.sockaddr = ngx_palloc(r->pool, zmp->zmpeer.socklen);
        if (zmp->zmpeer.sockaddr == NULL) {
            return; /* NO MEM */
        }
        ngx_memcpy(zmp->zmpeer.sockaddr, work->route->sockaddr, zmp->zmpeer.socklen);

    } else {
        ngx_log_error(NGX_LOG_WARN, r->connection->log, 0,
                "zmauth: an error occurs during zm lookup: %V, fall back to "
                "IPHASH to get the upstream route",
                &work->err);
        /* fallback to IPHASH (bug 54641, bug 52553) */
        zmp->zmroutetype = zmroutetype_fallback;
        /* Client IP not allowed, need to be thrown a 403 (bug 55152) */
        if (work->err.len && ngx_strstr(work->err.data, NGX_ACCESS_DENIED_ERRMSG.data)) {
            zmp->access_denied = 1;
        }
    }

    void (*connect_func)(ngx_http_request_t*, ngx_http_upstream_t*) = ctx->connect;

    ngx_destroy_pool(ctx->pool);
    ngx_http_set_ctx(r, NULL, ngx_http_upstream_zmauth_module);

    /* bug 64775, 62374, we have to invoke "connect" at last statement */
    connect_func(r, r->upstream); /* async invoke ngx_http_upstream_connect */
}

static void
ngx_http_upstream_free_zmauth_peer(ngx_peer_connection_t *pc,
        void *data, ngx_uint_t state) {
    ngx_http_upstream_zmauth_peer_data_t *zmp = data;
    /* only handle the case when the upstream returned by zmlookup is within
     * upstream block in the config file
     */
    if (zmp->fp.current != NGX_INVALID_ARRAY_INDEX) {
        ngx_http_upstream_free_fair_peer(pc, &zmp->fp, state);
    }
}

/* examine a single request cookie for ZM_AUTH_TOKEN
 if present, fill in peer with the ip:port of the decoded mailhost (true)
 else return false
 */
#ifdef unused
static ngx_flag_t ngx_http_upstream_zmserver_from_cookie
(ngx_log_t *log, ngx_pool_t *pool, ngx_table_elt_t *cookie, ngx_addr_t *peer)
{
    ngx_str_t *cv = &cookie->value;
    u_char *p, *q, *start, *end;
    ngx_int_t z;
    ngx_str_t enc_token, enc_zmdata, dec_zmdata, ip, line;
    ngx_int_t part1, part2, part3;
    size_t i,j,qlen;
    ngx_flag_t ret;
    u_char *ZM_AUTH_TOKEN = (u_char *)"ZM_AUTH_TOKEN";
    const size_t ZMLEN = sizeof("ZM_AUTH_TOKEN")-1;

    ret = 0;

    start = cv->data;
    end = start + cv->len;
    p = start;

    /* cv will be of the form name=value; name=value; name=value; ... */
    while (p < end)
    {
        line.data = p;
        line.len = end - p;

        /* The latter part of the loop will ensure that at this point, `p'
         points to the start of a "NAME=VALUE" string
         */

        z = ngx_memn2cmp (p, ZM_AUTH_TOKEN, (size_t)(end-p) > ZMLEN ? ZMLEN : (size_t)(end-p), ZMLEN);

        if (z == 0)
        {
            /* match found
             the value against zm_auth_token is
             X_YYY_ZZZZZZZZZZ
             the X and Y parts must be ignored, and the Z part is hex-encoded
             after decoding the Z part, we can get a string like:
             id=36:cc00ce85-8c0b-49eb-8e08-a8aab43ce836;exp=13:1196504658160;type=6:zimbra;mailhost=14:127.0.0.1:7070;
             */

            p = p + ZMLEN;

            if (p < end)
            {
                /* There is some value against ZM_AUTH_TOKEN

                 TODO: research the RFC on the cookie header and see if spaces
                 are allowed between [NAME=VALUE], as in [NAME = VALUE]
                 */
                if (*p == '=')
                {
                    ++p;

                    /* p is at (ZMAUTH_TOKEN=)VALUE
                     ^
                     build up enc_token containing the entire value
                     */

                    enc_token.data = p;

                    part2 = part3 = -1;
                    part1 = 0;

                    while (p < end && *p != ';' && !isspace(*p)) {
                        if (*p == '_') {
                            if (part2 < 0) {part2 = (p-enc_token.data) +1;}
                            else if (part3 < 0) {part3 = (p-enc_token.data) +1;}
                        }
                        ++p;
                    }

                    if (part3 < 0) {part3 = 0;}

                    enc_token.len = p - enc_token.data;

                    /* enc_token contains the entire hex-encoded auth-token,
                     we are interested in only the part after the second
                     underscore
                     */

                    enc_zmdata.data = enc_token.data + part3;
                    enc_zmdata.len = enc_token.len - part3;

                    /* now enc_zmdata contains the hex-encoded auth-token */
                    if (enc_zmdata.len % 2 == 1) {
                        ngx_log_error (NGX_LOG_ERR, log, 0,
                                "zmauth: odd bytes in hex-encoded zmauth: enc=[%V], len=[%d]",
                                &enc_zmdata, enc_zmdata.len
                        );
                    } else {
                        /* now hex-decode the thingy */
                        dec_zmdata.data = ngx_palloc (pool, enc_zmdata.len/2 +1); // +1 for null
                        dec_zmdata.len = enc_zmdata.len/2;

                        for (i =0, j=0; i<enc_zmdata.len; i=i+2, j=j+1) {
                            if (enc_zmdata.data[i] >= '0' && enc_zmdata.data[i] <= '9') {
                                dec_zmdata.data[j] = enc_zmdata.data[i] - '0';
                            } else {
                                dec_zmdata.data[j] = 10 + tolower (enc_zmdata.data[i]) - 'a';
                            }
                            dec_zmdata.data[j] <<= 4;
                            if (enc_zmdata.data[i+1] >= '0' && enc_zmdata.data[i+1] <= '9') {
                                dec_zmdata.data[j] += (enc_zmdata.data[i+1] - '0');
                            } else {
                                dec_zmdata.data[j] += 10 + tolower (enc_zmdata.data[i+1]) - 'a';
                            }
                        }

                        dec_zmdata.data[j] =0;

                        /* The decoded data looks like (on a single line) -

                         id=36:cc00ce85-8c0b-49eb-8e08-a8aab43ce836;
                         exp=13:1196504658160;
                         type=6:zimbra;
                         mailhost=14:127.0.0.1:7070;

                         semicolon separated list of strings of the form
                         field=len:value

                         */

                        ngx_log_debug1 (NGX_LOG_DEBUG_HTTP, log, 0,
                                "zmauth: decode(ZM_AUTH_TOKEN):[%V]", &dec_zmdata
                        );

                        /* now we set up a loop to locate the mailhost */
                        q = (u_char *) ngx_strstr (dec_zmdata.data, "mailhost=");

                        if (q != NULL) {
                            q += sizeof("mailhost=") -1;
                            // now q will point to the length: portion of the ipaddress:port
                            qlen = 0;
                            while (*q != ':') { // XXX: no bounds check - too far in
                                qlen = (qlen*10) + (*q-'0');
                                ++q;
                            }
                            ++q; // consume ':'
                            ip.data = q;
                            ip.len = qlen;

                            /* now ip contains the ip-address:port of the upstream */
                            ngx_log_debug1 (NGX_LOG_DEBUG_HTTP, log, 0,
                                    "zmauth: mailhost(ZM_AUTH_TOKEN):[%V]", &ip
                            );

                            *peer = *deserialize_peer_ipv4 (ip.data, ip.len, pool);
                            ret=1;
                        }
                    }
                }
            }

        } else {
            while (p < end && *p!=';') {++p;}
            if (p < end) {
                ++p; // consume `;'
                while (p < end && isspace (*p)) {++p;}
            } else {
                /* we have reached the end of the cookie string */
                continue;
            }
        }
    }

    return ret;
}
#endif

static ngx_flag_t
ngx_get_cookie_value(ngx_log_t *log,
        ngx_table_elt_t **cookies, ngx_uint_t ncookies, ngx_str_t *name,
        ngx_str_t *value) {
    ngx_table_elt_t **c;
    u_char *s, *p, *e;
    ngx_str_t V, n, v;
    ngx_flag_t f;

    for (c = cookies, f = 0; c < cookies + ncookies && f == 0; ++c) {
        V = (*c)->value;
        /* v is of the form "name=value; name=value;" */
        s = V.data;
        e = s + V.len;
        p = s;

        ngx_log_debug1(NGX_LOG_DEBUG_HTTP, log, 0,
                "zmauth: examining cookie value:%V",&V);

        while (p < e) {
            n.data = p;
            while (p < e && *p != '=') {
                ++p;
            }
            if (p == e) {
                break;
            }
            n.len = p - n.data;
            ++p; // consume =
            v.data = p;
            while (p < e && *p != ';') {
                ++p;
            }
            v.len = p - v.data;
            if (n.len == name->len && ngx_memcmp(n.data, name->data, n.len)
                    == 0) {
                *value = v;
                f = 1;
                break;
            }
            if (p == e) {
                break;
            }
            ++p; // consume ;
            while (p < e && (*p == ' ' || *p == '\t')) {
                ++p;
            }
        }
    }

    return f;
}

static ngx_flag_t ngx_get_query_string_arg(ngx_log_t *log, ngx_str_t *args,
        ngx_str_t *name, ngx_str_t *value) {
    ngx_flag_t f = 0;
    u_char *f1, *f2, *v1, *v2, *s, *e, *p;

    ngx_log_debug2(NGX_LOG_DEBUG_HTTP,log,0,
            "zmauth: examing query-string %V for field:%V", args, name);

    s = args->data;
    e = s + args->len;

    for (p = s; p < e;) {
        f1 = f2 = v1 = v2 = p;

        /* we are at the start of name=value */

        while (*p != '=' && p < e) {
            ++p;
        }

        f2 = p;
        if (p == e) {
            break;
        }
        ++p;

        v1 = p;
        v2 = v1;
        if (p == e) {
            break;
        }

        while (*p != '&' && p < e) {
            ++p;
        }

        v2 = p;

        if (f2 == f1 + name->len && ngx_memcmp(f1, name->data, f2 - f1) == 0) {
            value->data = v1;
            value->len = v2 - v1;
            ngx_log_debug3(NGX_LOG_DEBUG_HTTP,log,0,
                    "zmauth: found value:%V against arg:%V in query-string:%V",
                    value, name, args);
            f = 1;
            break;
        }

        if (p == e) {
            break;
        }

        ++p;
    }

    return f;
}

/* extract a field from ZM_AUTH_TOKEN */
static ngx_flag_t
ngx_field_from_zmauthtoken(ngx_log_t *log, ngx_pool_t *pool,
        ngx_str_t *authtoken, ngx_str_t *field, ngx_str_t *value) {
    ngx_str_t T2, t2;
    u_char *p, *s, *e;
    ngx_uint_t t;
    ngx_flag_t f;
    ngx_str_t F, V;
    ngx_uint_t i, j, l;

    s = authtoken->data;
    e = s + authtoken->len;

    p = s;

    for (p = s, t = 0, f = 0; p < e && f == 0; ++p) {
        if (*p == '_') {
            if (t == 1) {
                T2.data = p + 1;
                T2.len = e - T2.data;
                f = 1;
            } else {
                ++t;
            }
        }
    }

    if (f == 0) {
        ngx_log_error(NGX_LOG_INFO,log,0,
                "zmauth: auth-token:%V does not contain 3 fields",
                authtoken);

        return 0;
    }

    /* hex-decode T2 to t2 */

    if (T2.len % 2 != 0) {
        ngx_log_error(NGX_LOG_INFO, log, 0,
                "zmauth: auth-token(#2):%V is invalid hex",
                &T2);

        return 0;
    }

    t2.len = T2.len / 2;
    t2.data = ngx_palloc(pool, t2.len);

    if (t2.data == NULL) {
        /* nomem */
        return 0;
    }

    for (i = 0, j = 0; i < T2.len; i = i + 2, j = j + 1) {
        if (T2.data[i] >= '0' && T2.data[i] <= '9') {
            t2.data[j] = T2.data[i] - '0';
        } else {
            t2.data[j] = 10 + tolower(T2.data[i]) - 'a';
        }
        t2.data[j] <<= 4;
        if (T2.data[i + 1] >= '0' && T2.data[i + 1] <= '9') {
            t2.data[j] += (T2.data[i + 1] - '0');
        } else {
            t2.data[j] += (10 + tolower(T2.data[i + 1]) - 'a');
        }
    }

    /* t2 now contains the entire decoded portion #2 of the auth token */

    ngx_log_debug1(NGX_LOG_DEBUG_ZIMBRA, log, 0,
            "zmauth: decoded(auth-token(#2)): %V",
            &t2);

    /* now we need to search for the named field 
     the decoded portion of the authtoken(#2) looks like
     field=len:value;field=len:value;...
     */

    s = t2.data;
    e = s + t2.len;
    f = 0;
    p = s;

    while (p < e) {
        F.data = p;
        while (p < e && *p != '=') {
            ++p;
        }
        if (p == e) {
            break;
        }
        F.len = p - F.data;
        l = 0;
        ++p; // consume =
        while (p < e && (*p >= '0' && *p <= '9')) {
            l = (l * 10) + (*p - '0');
            ++p;
        }
        if (p == e) {
            break;
        }
        if (*p != ':') {
            break;
        }
        ++p; // consume :
        V.data = p;
        while (p < e && p < V.data + l) {
            ++p;
        }
        if (p != V.data + l) {
            break;
        }
        V.len = l;

        if (F.len == field->len && ngx_memcmp(field->data, F.data, F.len) == 0) {
            f = 1;
            *value = V;
            ngx_log_debug3(NGX_LOG_DEBUG_ZIMBRA, log, 0,
                    "zmauth: auth-token(field=%V,len=%d,value=%V)", &F, V.len,
                    &V);
            break;
        }

        if (p < e) {
            ++p;
        } // consume ;
    }

    return f;
}

/* extract the jwt token from Header*/
static ngx_flag_t
ngx_get_authheader_bearer(ngx_log_t *log, ngx_pool_t *pool,
        ngx_http_headers_in_t *headers_in, ngx_str_t *value) {
    ngx_log_debug0 (NGX_LOG_DEBUG_HTTP, log, 0,
            "zmauth: ngx_get_authheader_bearer entered");

    ngx_str_t authValue;
    ngx_str_t token;

    authValue = headers_in->authorization->value;

    ngx_log_debug1 (NGX_LOG_DEBUG_HTTP, log, 0,
            "zmauth: ngx_get_authheader_bearer token:%V", &authValue);

    if (authValue.len >= sizeof("Bearer ") - 1
            && ngx_memcmp(authValue.data,"Bearer ",sizeof("Bearer ")-1)
            == 0) {
        ngx_log_debug0 (NGX_LOG_DEBUG_HTTP, log, 0,
                "zmauth: ngx_get_authheader_bearer Bearer token found");

        token = authValue;
        token.data += (sizeof("Bearer ") - 1);
        token.len -= (sizeof("Bearer ") - 1);

        ngx_log_debug1 (NGX_LOG_DEBUG_HTTP, log, 0,
                "zmauth: ngx_get_authheader_bearer Bearer token found:%V", &token);
        *value = token;

        return 1; 
    }

    ngx_log_debug0 (NGX_LOG_DEBUG_HTTP, log, 0,
            "zmauth: ngx_get_authheader_bearer exit");

    return 0;
}

/* extract claim data from jwt token */
static ngx_flag_t
ngx_claimdata_from_jwttoken(ngx_log_t *log, ngx_pool_t *pool,
        ngx_str_t *authtoken, ngx_str_t *field, ngx_str_t *value) {
    ngx_flag_t f;
    ngx_log_debug0 (NGX_LOG_DEBUG_HTTP, log, 0,
            "zmauth: ngx_claimdata_from_jwttoken entered");

    ngx_str_t pattern = ngx_string("(?<=\\.)(.*?)(?=\\.)");
    ngx_regex_compile_t rgc;
    u_char errstr[NGX_MAX_CONF_ERRSTR];
    ngx_memzero(&rgc, sizeof(ngx_regex_compile_t));

    rgc.pattern  = pattern;
    rgc.pool     = pool;
    rgc.err.len  = NGX_MAX_CONF_ERRSTR;
    rgc.err.data = errstr;
    if (ngx_regex_compile(&rgc) != NGX_OK) {
        ngx_log_error(NGX_LOG_INFO, log, 0,
                "zmauth: ngx_claimdata_from_jwttoken regex compilation failed. Error:%s", errstr);
        return 0;
    }

    int captures[(1 + rgc.captures) * 3];
    ngx_int_t  n;

    n = ngx_regex_exec(rgc.regex, authtoken, captures, (1 + rgc.captures) * 3);
    if (n >= 0) {
        /* string matches expression */
        ngx_log_debug0(NGX_LOG_DEBUG_ZIMBRA, log, 0,
                "zmauth: ngx_claimdata_from_jwttoken match found");
        ngx_str_t encodedPayload;
        encodedPayload.data = authtoken->data + captures[0];
        encodedPayload.len = captures[1] - captures[0];
        ngx_log_debug1(NGX_LOG_DEBUG_ZIMBRA, log, 0,
                "zmauth: ngx_claimdata_from_jwttoken payload is %V", &encodedPayload);

        ngx_str_t urlDecodedPayload;
        urlDecodedPayload.data = ngx_pnalloc(pool, ngx_base64_decoded_length(encodedPayload.len));
        if (urlDecodedPayload.data == NULL) {
            ngx_log_error(NGX_LOG_INFO, log, 0,
                    "zmauth: ngx_claimdata_from_jwttoken memory allocation from pool failed");
            return NGX_ERROR;
        }

        if (ngx_decode_base64url(&urlDecodedPayload, &encodedPayload) != NGX_OK) {
            ngx_log_error(NGX_LOG_INFO, log, 0,
                    "zmauth: ngx_claimdata_from_jwttoken base64url decoding failed");
            return 0;
        }
        ngx_log_debug1(NGX_LOG_DEBUG_ZIMBRA, log, 0,
                "zmauth: ngx_claimdata_from_jwttoken base64url decoded payload is %V", &urlDecodedPayload);
        int ret = ngx_claimdata_from_payload(log,pool,&urlDecodedPayload,value);
        return ret;
    }
    else if (n == NGX_REGEX_NO_MATCHED) {
        /* no match was found */
        ngx_log_debug0(NGX_LOG_DEBUG_ZIMBRA, log, 0,
                "zmauth: ngx_claimdata_from_jwttoken no match found");
        return 0;      
    }
    else {
        /* some error */
        ngx_log_debug1(NGX_LOG_DEBUG_ZIMBRA, log, 0,
                "zmauth: ngx_claimdata_from_jwttoken failed: %i", n);
        return 0;
    }

    ngx_log_debug0 (NGX_LOG_DEBUG_HTTP, log, 0,
            "zmauth: ngx_claimdata_from_jwttoken exit");
 
    return 0;
}

/* extract sub data field from payload */
static ngx_flag_t
ngx_claimdata_from_payload(ngx_log_t *log, ngx_pool_t *pool,
        ngx_str_t *payload, ngx_str_t *value) {
    ngx_flag_t f;
    ngx_log_debug0 (NGX_LOG_DEBUG_HTTP, log, 0,
            "zmauth: ngx_claimdata_from_payload entered");

    ngx_str_t pattern = ngx_string("\"sub\":[\\s]*\"(.*?)\"[\\s]*");
    ngx_regex_compile_t rgc;
    u_char errstr[NGX_MAX_CONF_ERRSTR];
    ngx_memzero(&rgc, sizeof(ngx_regex_compile_t));

    rgc.pattern  = pattern;
    rgc.pool     = pool;
    rgc.err.len  = NGX_MAX_CONF_ERRSTR;
    rgc.err.data = errstr;
    if (ngx_regex_compile(&rgc) != NGX_OK) {
        ngx_log_error(NGX_LOG_INFO, log, 0,
                "zmauth: ngx_claimdata_from_payload regex compilation failed. Error:%s", errstr);
        return 0;
    }

    int captures[(1 + rgc.captures) * 3];
    ngx_int_t  n;

    n = ngx_regex_exec(rgc.regex, payload, captures, (1 + rgc.captures) * 3);
    if (n >= 0) {
        /* string matches expression */
        ngx_log_debug0(NGX_LOG_DEBUG_ZIMBRA, log, 0,
                "zmauth: ngx_claimdata_from_payload match found");
        ngx_str_t subData;
        subData.data = payload->data + captures[2];
        subData.len = captures[3] - captures[2];
        ngx_log_debug1(NGX_LOG_DEBUG_ZIMBRA, log, 0,
                "zmauth: ngx_claimdata_from_payload subData is %V", &subData);
        *value = subData;
        return 1;
    }
    else if (n == NGX_REGEX_NO_MATCHED) {
        /* no match was found */
        ngx_log_debug0(NGX_LOG_DEBUG_ZIMBRA, log, 0,
                "zmauth: ngx_claimdata_from_payload no match found");
        return 0;      
    }
    else {
        /* some error */
        ngx_log_debug1(NGX_LOG_DEBUG_ZIMBRA, log, 0,
                "zmauth: ngx_claimdata_from_jwttoken failed: %i", n);
        return 0;
    }

    ngx_log_debug0 (NGX_LOG_DEBUG_HTTP, log, 0,
            "zmauth: ngx_claimdata_from_payload exit");
 
    return 0;
}

static void *
ngx_http_upstream_zmauth_create_srv_conf(ngx_conf_t *cf) {
    ngx_http_upstream_zmauth_srv_conf_t *zscf;

    zscf = ngx_pcalloc(cf->pool, sizeof(ngx_http_upstream_zmauth_srv_conf_t));
    if (zscf == NULL) {
        return NGX_CONF_ERROR;
    }

    return zscf;
}

static char *
ngx_http_upstream_zmauth_merge_srv_conf(ngx_conf_t *cf, void *parent,
        void *child) {
    ngx_http_upstream_zmauth_srv_conf_t *prev = parent;
    ngx_http_upstream_zmauth_srv_conf_t *conf = child;

    ngx_conf_merge_value(conf->dummy, prev->dummy, 0);

    return NGX_CONF_OK;
}

/* examine the request uri for zimbra REST patterns
 currently supported patterns -

 /home/user/content
 /home/~/content
 /home/~user/content
 /service/home/user/content
 /service/home/~/content
 /service/home/~user/content

 return true(1) if indeed the request URI matches a REST pattern
 also fill in usr with the correct usr if so

 usr is blanked out before processing begins
 refer ZimbraServer/docs/rest.txt for details
 */
static ngx_flag_t
zmauth_check_rest(ngx_http_request_t *r, void **extra) {
    ngx_flag_t f;
    u_char *p;
    ngx_log_t *log;
    ngx_pool_t *pool;
    ngx_str_t ausr, *usr;

    f = 0;
    pool = r->pool;
    log = r->connection->log;

    ausr.data = (u_char*) "";
    ausr.len = 0;

    ngx_log_debug1(NGX_LOG_DEBUG_HTTP, log, 0,
            "zmauth: examining uri:%V for REST", &r->uri);

    if (r->uri.len >= sizeof("/home/~/") - 1
            && ngx_memcmp(r->uri.data,"/home/~/", sizeof("/home/~/") - 1) == 0) {
        f = 0; /* for /home/~/ route will be discovered from the zm_auth_token */
    } else if (r->uri.len >= sizeof("/home/~") - 1
            && ngx_memcmp(r->uri.data,"/home/~", sizeof("/home/~") - 1) == 0) {
        ausr.data = r->uri.data + (sizeof("/home/~") - 1);
        for (p = ausr.data; p < r->uri.data + r->uri.len; ++p) {
            if (*p == '/') {
                f = 1;
                break;
            }
        }
        ausr.len = p - ausr.data;
    } else if (r->uri.len >= sizeof("/home/") - 1
            && ngx_memcmp(r->uri.data,"/home/",sizeof("/home/") - 1) == 0) {
        ausr.data = r->uri.data + (sizeof("/home/") - 1);
        for (p = ausr.data; p < r->uri.data + r->uri.len; ++p) {
            if (*p == '/') {
                f = 1;
                break;
            }
        }
        ausr.len = p - ausr.data;
    } else if (r->uri.len >= sizeof("/service/home/~/") - 1
            && ngx_memcmp(r->uri.data,"/service/home/~/", sizeof("/service/home/~/") - 1)
                    == 0) {
        f = 0; /* for /service/home/~/ route will be discovered from the zm_auth_token */
    } else if (r->uri.len >= sizeof("/service/home/~") - 1
            && ngx_memcmp(r->uri.data,"/service/home/~", sizeof("/service/home/~") - 1)
                    == 0) {
        ausr.data = r->uri.data + (sizeof("/service/home/~") - 1);
        for (p = ausr.data; p < r->uri.data + r->uri.len; ++p) {
            if (*p == '/') {
                f = 1;
                break;
            }
        }
        ausr.len = p - ausr.data;
    } else if (r->uri.len >= sizeof("/service/home/") - 1
            && ngx_memcmp(r->uri.data, "/service/home/", sizeof("/service/home/") - 1)
                    == 0) {
        ausr.data = r->uri.data + (sizeof("/service/home/") - 1);
        for (p = ausr.data; p < r->uri.data + r->uri.len; ++p) {
            if (*p == '/') {
                f = 1;
                break;
            }
        }
        ausr.len = p - ausr.data;
    }

    if (f) {
        if (ausr.len == 0) {
            f = 0;
        }
    }

    if (f) {
        usr = ngx_palloc(pool, sizeof(ngx_str_t));
        if (usr == NULL) {
            f = 0;
        } else {
            *usr = ausr;
            *extra = usr;
        }
    }

    if (f) {
        ngx_log_debug2(NGX_LOG_DEBUG_HTTP,log,0,
                "uri:%V matched a REST pattern, user:%V", &r->uri, &ausr);
    }

    return f;
}

static ngx_flag_t
zmauth_check_activesync(ngx_http_request_t *r, void **extra) {
    ngx_log_t *log;
    ngx_pool_t *pool;
    ngx_str_t authval, cred64, cred, credusr, *usr;
    u_char *p;
    ngx_flag_t rc;
    ngx_str_t userArg = ngx_string("User");

    rc = 0;
    log = r->connection->log;
    pool = r->pool;

    ngx_log_debug1(NGX_LOG_DEBUG_HTTP,log,0,
            "zmauth: examining uri:%V for ActiveSync", &r->uri);

    if (r->uri.len >= sizeof("/Microsoft-Server-ActiveSync") - 1
            && ngx_memcmp(r->uri.data,"/Microsoft-Server-ActiveSync",sizeof("/Microsoft-Server-ActiveSync")-1)
                    == 0) {
        if (r->headers_in.authorization != NULL
                && r->headers_in.authorization->value.data != NULL) {
            ngx_log_debug1(NGX_LOG_DEBUG_HTTP,log,0,
                    "ActiveSync: Found RFC 2617 authorization header: %V",
                    &r->headers_in.authorization->value);
            authval = r->headers_in.authorization->value;
            if (authval.len >= sizeof("Basic ") - 1
                    && ngx_memcmp(authval.data,"Basic ",sizeof("Basic ")-1)
                            == 0) {
                cred64 = authval;
                cred64.data += (sizeof("Basic ") - 1);
                cred64.len -= (sizeof("Basic ") - 1);
                cred.len = ngx_base64_decoded_length(cred64.len);
                cred.data = ngx_palloc(pool, cred.len);
                if (cred.data != NULL) {
                    if (ngx_decode_base64(&cred, &cred64) == NGX_OK) {

#if (NGX_DEBUG_HTTP_PASSWD)
     ngx_log_debug1(NGX_LOG_DEBUG_HTTP,log,0,
                    "ActiveSync: found auth basic credentials: %V", &cred);
#endif

                        /* (RFC 2617)

                         basic-credentials = base64-user-pass
                         base64-user-pass  = <base64 [4] encoding of user-pass,
                         except not limited to 76 char/line>
                         user-pass   = userid ":" password
                         userid      = *<TEXT excluding ":">
                         password    = *TEXT
                         */

                        credusr.data = cred.data;
                        p = cred.data;
                        while (p < cred.data + cred.len && *p != ':') {
                            ++p;
                        }
                        credusr.len = p - cred.data;
                        usr = ngx_palloc(pool, sizeof(ngx_str_t));

                        if (usr != NULL) {
                            zmauth_translate_activesync_ews_usr(pool, &credusr, usr);
                            ngx_log_debug2(NGX_LOG_DEBUG_HTTP,log,0,
                                    "ActiveSync: user:%V translated to user:%V for route discovery",
                                    &credusr,usr);

                            *extra = usr;
                            rc = 1;
                        }
                    }
                }
            }

        } else {
            ngx_log_debug1(NGX_LOG_DEBUG_HTTP,log,0,
                    "ActiveSync: No authorization header, examine args: [%V]",
                    &r->args);

            usr = ngx_palloc(pool, sizeof(ngx_str_t));
            if (usr != NULL && zmauth_find_arg(&r->args, &userArg, usr) != 0) {
                ngx_log_debug1(NGX_LOG_DEBUG_HTTP,log,0,
                        "ActiveSync: fallback to HTTP argument User1:%V",
                        usr);

                *extra = usr;
                rc = 1;
            }
        }
    }

    return rc;
}

static ngx_flag_t
zmauth_check_ews(ngx_http_request_t *r, void **extra) {
    ngx_log_t *log;
    ngx_pool_t *pool;
    ngx_str_t authval, cred64, cred, credusr, *usr;
    u_char *p;
    ngx_flag_t rc;
    ngx_str_t userArg = ngx_string("User");

    rc = 0;
    log = r->connection->log;
    pool = r->pool;

    ngx_log_debug1(NGX_LOG_DEBUG_HTTP,log,0,
            "zmauth: examining uri:%V for EWS", &r->uri);

    if (r->uri.len >= sizeof("/ews/Exchange.asmx") - 1
            && ngx_strncasecmp(r->uri.data, (u_char *)"/ews/Exchange.asmx", sizeof("/ews/Exchange.asmx")-1)
                    == 0) {
        if (r->headers_in.authorization != NULL
                && r->headers_in.authorization->value.data != NULL) {
            ngx_log_debug1(NGX_LOG_DEBUG_HTTP,log,0,
                    "EWS: Found RFC 2617 authorization header: %V",
                    &r->headers_in.authorization->value);
            authval = r->headers_in.authorization->value;
            if (authval.len >= sizeof("Basic ") - 1
                    && ngx_memcmp(authval.data,"Basic ",sizeof("Basic ")-1)
                            == 0) {
                cred64 = authval;
                cred64.data += (sizeof("Basic ") - 1);
                cred64.len -= (sizeof("Basic ") - 1);
                cred.len = ngx_base64_decoded_length(cred64.len);
                cred.data = ngx_palloc(pool, cred.len);
                if (cred.data != NULL) {
                    if (ngx_decode_base64(&cred, &cred64) == NGX_OK) {

#if (NGX_DEBUG_HTTP_PASSWD)
     ngx_log_debug1(NGX_LOG_DEBUG_HTTP,log,0,
                    "EWS: found auth basic credentials: %V", &cred);
#endif

                        /* (RFC 2617)

                         basic-credentials = base64-user-pass
                         base64-user-pass  = <base64 [4] encoding of user-pass,
                         except not limited to 76 char/line>
                         user-pass   = userid ":" password
                         userid      = *<TEXT excluding ":">
                         password    = *TEXT
                         */

                        credusr.data = cred.data;
                        p = cred.data;
                        while (p < cred.data + cred.len && *p != ':') {
                            ++p;
                        }
                        credusr.len = p - cred.data;
                        usr = ngx_palloc(pool, sizeof(ngx_str_t));

                        if (usr != NULL) {
                            zmauth_translate_activesync_ews_usr(pool, &credusr, usr);
                            ngx_log_debug2(NGX_LOG_DEBUG_HTTP,log,0,
                                    "EWS: user:%V translated to user:%V for route discovery",
                                    &credusr,usr);

                            *extra = usr;
                            rc = 1;
                        }
                    }
                }
            }

        } else {
            ngx_log_debug1(NGX_LOG_DEBUG_HTTP,log,0,
                    "EWS: No authorization header, examine args: [%V]",
                    &r->args);

            usr = ngx_palloc(pool, sizeof(ngx_str_t));
            if (usr != NULL && zmauth_find_arg(&r->args, &userArg, usr) != 0) {
                ngx_log_debug1(NGX_LOG_DEBUG_HTTP,log,0,
                        "EWS: fallback to HTTP argument User1:%V",
                        usr);

                *extra = usr;
                rc = 1;
            }
        }
    }

    return rc;
}

static ngx_flag_t
zmauth_check_caldav(ngx_http_request_t *r, void **extra) {
    ngx_log_t *log;
    ngx_pool_t *pool;
    ngx_str_t *usr, ausr = ngx_string("");
    u_char *p;
    ngx_flag_t f;

    f = 0;
    log = r->connection->log;
    pool = r->pool;

    ngx_log_debug1(NGX_LOG_DEBUG_HTTP,log,0,
            "zmauth: examining uri:%V for caldav", &r->uri);

    if (r->uri.len >= sizeof("/dav/") - 1
            && ngx_memcmp(r->uri.data,"/dav/",sizeof("/dav/") - 1) == 0) {
        ausr.data = r->uri.data + (sizeof("/dav/") - 1);
        for (p = ausr.data; p < r->uri.data + r->uri.len; ++p) {
            if (*p == '/') {
                f = 1;
                break;
            }
        }
        ausr.len = p - ausr.data;
    } else if (r->uri.len >= sizeof("/principals/users/") - 1
            && ngx_memcmp(r->uri.data,"/principals/users/", sizeof("/principals/users/") - 1)
                    == 0) {
        ausr.data = r->uri.data + (sizeof("/principals/users/") - 1);
        for (p = ausr.data; p < r->uri.data + r->uri.len; ++p) {
            if (*p == '/') {
                f = 1;
                break;
            }
        }
        ausr.len = p - ausr.data;
    }

    if (f) {
        if (ausr.len == 0) {
            f = 0;
        }
    }

    if (f) {
        usr = ngx_palloc(pool, sizeof(ngx_str_t));
        if (usr == NULL) {
            f = 0;
        } else {
            *usr = ausr;
            *extra = usr;
        }
    }

    if (f) {
        ngx_log_debug2(NGX_LOG_DEBUG_HTTP,log,0,
                "uri:%V matched caldav, user:%V", &r->uri,&ausr);
    }

    return f;
}


/* examine request cookies for ZM_AUTH_TOKEN and extract route if so */
static ngx_flag_t
zmauth_check_authtoken(ngx_http_request_t *r, ngx_str_t* field,
		void **extra) {
    ngx_pool_t *pool;
    ngx_log_t *log;
    ngx_str_t token, value, *pvalue;
    ngx_flag_t f;

    pool = r->pool;
    log = r->connection->log;

    ngx_log_debug0 (NGX_LOG_DEBUG_HTTP, log, 0,
            "zmauth: search for ZM_AUTH_TOKEN");

    /* look for auth token in the request cookie(s) */
    f = ngx_get_cookie_value(log,
            (ngx_table_elt_t **) r->headers_in.cookies.elts,
            r->headers_in.cookies.nelts, &NGX_ZMAUTHTOKEN, &token);

    if (!f) {
        /* if not found, then look in the zauthtoken= query string arg */
        f = ngx_get_query_string_arg(log, &r->args, &NGX_ZAUTHTOKEN, &token);
    }

    if (f) {
        ngx_log_debug1 (NGX_LOG_DEBUG_HTTP, log, 0,
                "zmauth: found ZM_AUTH_TOKEN:%V",
                &token);

        f = ngx_field_from_zmauthtoken(log, pool, &token, field, &value);
        if (f) {
            ngx_log_debug2 (NGX_LOG_DEBUG_HTTP, log, 0,
                    "zmauth: got %V:%V from ZM_AUTH_TOKEN",
                    field, &value);
            if (value.len > 0) {
                pvalue = ngx_palloc(pool, sizeof(ngx_str_t));
                if (pvalue == NULL) {
                    f = 0;
                } else {
                    pvalue->data = ngx_pstrdup(pool, &value); /* TODO: shallowcopy? */
                    if (pvalue->data == NULL) {
                        f = 0;
                    } else {
                        pvalue->len = value.len;
                        *((ngx_str_t**) extra) = pvalue;
                    }
                }
            } else {
                f = 0;
            }
        } else {
            ngx_log_debug1 (NGX_LOG_DEBUG_HTTP, log, 0,
                    "zmauth: no %V in ZM_AUTH_TOKEN", field);
        }

    } else {
        ngx_log_debug1 (NGX_LOG_DEBUG_HTTP, log, 0,
                "zmauth: no ZM_AUTH_TOKEN",
                &token);
    }

    return f;
}

/* examine request header and query parameter for jwt token and extract route if so */
static ngx_flag_t
zmauth_check_jwttoken(ngx_http_request_t *r, ngx_str_t* field,
		void **extra) {
    ngx_pool_t *pool;
    ngx_log_t *log;
    ngx_str_t token, value, *pvalue;
    ngx_flag_t f;

    pool = r->pool;
    log = r->connection->log;
    ngx_log_debug0 (NGX_LOG_DEBUG_HTTP, log, 0, "zmauth:zmauth_check_jwttoken starts");
    //Bearer header extraction starts
    if (r->headers_in.authorization != NULL
            && r->headers_in.authorization->value.data != NULL) {
        ngx_log_debug0 (NGX_LOG_DEBUG_HTTP, log, 0,
                "zmauth:zmauth_check_jwttoken authorization header exists");
        f = ngx_get_authheader_bearer(log, pool, &r->headers_in, &token);
    }
    //Bearer header extraction ends

    if (!f) {
        /* if not found, then look in the query string arg zjwt*/
        f = ngx_get_query_string_arg(log, &r->args, &NGX_ZJWT_QUERY, &token);
    }

    if (f) {
        ngx_log_debug1 (NGX_LOG_DEBUG_HTTP, log, 0,
                "zmauth:zmauth_check_jwttoken found ZM_JWT_TOKEN:%V", &token);

        f = ngx_claimdata_from_jwttoken(log, pool, &token, field, &value);

        if (f) {
            ngx_log_debug2 (NGX_LOG_DEBUG_HTTP, log, 0,
                    "zmauth: got %V:%V from ZM_AUTH_TOKEN", field, &value);
            if (value.len > 0) {
                pvalue = ngx_palloc(pool, sizeof(ngx_str_t));
                if (pvalue == NULL) {
                    f = 0;
                } else {
                    pvalue->data = ngx_pstrdup(pool, &value); /* TODO: shallowcopy? */
                    if (pvalue->data == NULL) {
                        f = 0;
                    } else {
                        pvalue->len = value.len;
                        *((ngx_str_t**) extra) = pvalue;
                    }
                }
            } else {
                f = 0;
            }
        } else {
            ngx_log_debug1 (NGX_LOG_DEBUG_HTTP, log, 0,
                    "zmauth: no %V in ZM_AUTH_TOKEN", field);
        }

    } else {
        ngx_log_debug1 (NGX_LOG_DEBUG_HTTP, log, 0,
                "zmauth: no ZM_AUTH_TOKEN",
                &token);
    }

    ngx_log_debug0 (NGX_LOG_DEBUG_HTTP, log, 0, "zmauth:zmauth_check_jwttoken ends");
    return f;
}



/* examine request cookies for ZM_ADMIN_AUTH_TOKEN and extract route if so */
static ngx_flag_t
zmauth_check_admin_authtoken(ngx_http_request_t *r, ngx_str_t* field,
        void **extra) {
    ngx_pool_t *pool;
    ngx_log_t *log;
    ngx_str_t token, value, *pvalue;
    ngx_flag_t f;

    pool = r->pool;
    log = r->connection->log;

    ngx_log_debug0 (NGX_LOG_DEBUG_HTTP, log, 0,
            "zmauth: search for ZM_ADMIN_AUTH_TOKEN");

    /* look for auth token in the request cookie(s) */
    f = ngx_get_cookie_value(log,
            (ngx_table_elt_t **) r->headers_in.cookies.elts,
            r->headers_in.cookies.nelts, &NGX_ZMAUTHTOKEN_ADMIN, &token);

    if (f) {
        ngx_log_debug1 (NGX_LOG_DEBUG_HTTP, log, 0,
                "zmauth: found ZM_AUTH_TOKEN:%V",
                &token);

        f = ngx_field_from_zmauthtoken(log, pool, &token, field, &value);
        if (f) {
        	ngx_log_debug2 (NGX_LOG_DEBUG_HTTP, log, 0,
        			"zmauth: got %V:%V from ZM_AUTH_TOKEN",
        			field, &value);

            if (value.len > 0) {
                pvalue = ngx_palloc(pool, sizeof(ngx_str_t));
                if (pvalue == NULL) {
                    f = 0;
                } else {
                    pvalue->data = ngx_pstrdup(pool, &value); /* TODO: shallowcopy? */
                    if (pvalue->data == NULL) {
                        f = 0;
                    } else {
                        pvalue->len = value.len;
                        *((ngx_str_t**) extra) = pvalue;
                    }
                }
            } else {
                f = 0;
            }
        } else {
            ngx_log_debug1 (NGX_LOG_DEBUG_HTTP, log, 0,
                    "zmauth: no %V in ZM_ADMIN_AUTH_TOKEN", field);
        }

    } else {
        ngx_log_debug1 (NGX_LOG_DEBUG_HTTP, log, 0,
                "zmauth: no ZM_ADMIN_AUTH_TOKEN",
                &token);
    }

    return f;
}

static zmroutetype_t
zmauth_check_uri(ngx_http_request_t *r, void **extra) {
    zmroutetype_t rtype;

    rtype = zmroutetype_fallback;
    if (zmauth_check_rest(r, extra)) {
        rtype = zmroutetype_rest;
        ngx_log_debug0(NGX_LOG_DEBUG_HTTP,r->connection->log,0,
                "zmauth: routing for REST");
    } else if (zmauth_check_activesync(r, extra)) {
        rtype = zmroutetype_activesync;
        ngx_log_debug0(NGX_LOG_DEBUG_HTTP,r->connection->log,0,
                "zmauth: routing for ActiveSync");
    } else if (zmauth_check_ews(r, extra)) {
        rtype = zmroutetype_ews;
        ngx_log_debug0(NGX_LOG_DEBUG_HTTP,r->connection->log,0,
                "zmauth: routing for EWS");
    } else if (zmauth_check_caldav(r, extra)) {
        rtype = zmroutetype_caldav;
        ngx_log_debug0(NGX_LOG_DEBUG_HTTP,r->connection->log,0,
                "zmauth: routing for caldav");
    } else if (zmauth_check_authtoken(r, &NGX_ZMAUTHTOKEN_ID, extra)) {
        rtype = zmroutetype_authtoken;
        ngx_log_debug0(NGX_LOG_DEBUG_HTTP,r->connection->log,0,
                "zmauth: routing by ZM_AUTH_TOKEN");
    } else if (zmauth_check_jwttoken(r, &NGX_ZMJWT_CLAIM_ID, extra)) {
        rtype = zmroutetype_jwttoken;
        ngx_log_debug0(NGX_LOG_DEBUG_HTTP,r->connection->log,0,
                "zmauth: routing by ZM_JWT_TOKEN");
    } else {
        ngx_log_debug0(NGX_LOG_DEBUG_HTTP,r->connection->log,0,
                "zmauth: routing by iphash");
    }
    return rtype;
}

static zmroutetype_t
zmauth_check_admin_uri(ngx_http_request_t *r, void **extra) {
    zmroutetype_t rtype;

    rtype = zmroutetype_fallback;
    if (zmauth_check_admin_authtoken(r, &NGX_ZMAUTHTOKEN_ID, extra)) {
        rtype = zmroutetype_authtoken;
        ngx_log_debug0(NGX_LOG_DEBUG_HTTP,r->connection->log,0,
                "zmauth: routing by ZM_ADMIN_AUTH_TOKEN");
    }
    return rtype;
}

/* translate an activesync/ews user rep to zimbra user rep
 domain\user becomes user@domain
 others remain identical
 */
static void
zmauth_translate_activesync_ews_usr(ngx_pool_t *pool, ngx_str_t *src,
        ngx_str_t *tgt) {
    u_char *p, *q;

    tgt->data = ngx_pstrdup(pool, src);
    if (tgt->data == NULL) {
        *tgt = *src;
        return;
    }

    tgt->len = src->len;
    p = src->data;

    while (p < src->data + src->len) {
        if (*p == '\\') {
            q = ngx_cpymem(tgt->data, p + 1, src->len - (p - src->data) - 1);
            *q++ = '@';
            q = ngx_cpymem(q, src->data, p - src->data);
            break;
        }
        ++p;
    }

    return;
}

/* extract an argument from query string args of the form n1=v1&n2=v2&n3=v3 */
static ngx_flag_t
zmauth_find_arg(/* const */ngx_str_t *args, /* const */
ngx_str_t *arg, ngx_str_t *val) {
    ngx_flag_t rc;
    u_char *p, *s, *e;
    ngx_str_t n, v;

    rc = 0;
    s = args->data;
    e = s + args->len;
    p = s;

    while (p < e) {
        n.data = p;
        while (p < e && *p != '=') {
            ++p;
        }
        if (p == e) {
            break;
        }
        n.len = p - n.data;

        ++p;
        v.data = p;

        while (p < e && *p != '&') {
            ++p;
        }
        if (p == e) {
            break;
        }

        v.len = p - v.data;
        ++p;

        if (n.len == arg->len && ngx_memcmp(n.data, arg->data, n.len) == 0) {
            *val = v;
            rc = 1;
            break;
        }
    }

    return rc;
}

/* find the upstream server returned by zmlookup in upstream block,
 * return NGX_MAX_UINT32_VALUE if not found */
static ngx_uint_t
zmauth_get_current_peer(ngx_http_upstream_zmauth_peer_data_t *zmp) {
    struct sockaddr_in *zmaddr, *peeraddr;
    struct sockaddr_in6 *zmaddr6, *peeraddr6;
    ngx_http_upstream_fair_peer_t *peer;
    ngx_uint_t i;

    for (i = 0; i < zmp->fp.peers->number; i++) {
        peer = &zmp->fp.peers->peer[i];

        if (zmp->zmpeer.sockaddr->sa_family != peer->sockaddr->sa_family) {
            continue;
        }

        if (zmp->zmpeer.sockaddr->sa_family == AF_INET) {
            zmaddr = (struct sockaddr_in *) zmp->zmpeer.sockaddr;
            peeraddr = (struct sockaddr_in *) peer->sockaddr;

            if (ngx_memcmp(&zmaddr->sin_addr, &peeraddr->sin_addr, 4) == 0
                    && zmaddr->sin_port == peeraddr->sin_port) {
                return i;
            }
        } else { /* AF_INET6 */
            zmaddr6 = (struct sockaddr_in6 *) zmp->zmpeer.sockaddr;
            peeraddr6 = (struct sockaddr_in6 *) peer->sockaddr;

            if (ngx_memcmp(&zmaddr6->sin6_addr, &peeraddr6->sin6_addr, 16) == 0
                    && zmaddr6->sin6_port == peeraddr6->sin6_port) {
                return i;
            }
        }
    }

    return NGX_INVALID_ARRAY_INDEX;
}

/* set the peer from zmlookup to peer connection */
static inline void
zmauth_set_peer(ngx_peer_connection_t *pc,
        ngx_http_upstream_zmauth_peer_data_t *zmp) {
    pc->sockaddr = zmp->zmpeer.sockaddr;
    pc->socklen = zmp->zmpeer.socklen;
    pc->name = &zmp->zmpeer.name;
}
