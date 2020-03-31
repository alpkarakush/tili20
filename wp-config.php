<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the
 * installation. You don't have to use the web site, you can
 * copy this file to "wp-config.php" and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * MySQL settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://codex.wordpress.org/Editing_wp-config.php
 *
 * @package WordPress
 */

// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'tili_db' );

/** MySQL database username */
define( 'DB_USER', 'root' );

/** MySQL database password */
define( 'DB_PASSWORD', '' );

/** MySQL hostname */
define( 'DB_HOST', 'localhost' );

/** Database Charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8mb4' );

/** The Database Collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );

/**#@+
 * Authentication Unique Keys and Salts.
 *
 * Change these to different unique phrases!
 * You can generate these using the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}
 * You can change these at any point in time to invalidate all existing cookies. This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define( 'AUTH_KEY',         '~cZ%STY:Qr!fxaa::`ci{_mNR*PJw,CkFkFSo HQz>}NH;S5L sl7rP*{Wvr)tc`' );
define( 'SECURE_AUTH_KEY',  'K%zL]+c4 .w@SHoMDb:Om& 1&1u+!p[~t`Qh0^w%9xj|n]p7;}Sj==Yr={VU,*R%' );
define( 'LOGGED_IN_KEY',    '2*_+w7fq^3YIj@miJYG5{hc-=~S;F8%Urs8] AxIPR_!#$/eBpzU}|VS^eY)6f]S' );
define( 'NONCE_KEY',        '5Ge?P-c{tNv^s66ejf<%#`-N(q8/nhv]FxL=b_3|4dTkjT7Y(&IFSwT5._e3fgC$' );
define( 'AUTH_SALT',        'k5BmIkPSW:SprgM?vQ;f|Ed~Kj+U[.{uSwyf=G*1n9}1Y<Av(#$U#gpwl^WQW,g&' );
define( 'SECURE_AUTH_SALT', 'a(BZ??>G+#w-dN$}VR[696sS0<rfNF;yF~&;{f5B#J]QVfxCH)e2G#x{&FF10:F(' );
define( 'LOGGED_IN_SALT',   '*TMcUDa|vYnd*FhpkZ9c4Al):Bp cX>j}IsSOZ}*,;!#9$cv*at{S`YEI~)!kAOw' );
define( 'NONCE_SALT',       '9V4Dk>OvzT3YHk$81YuW{Q6HT;f87oHJF%&/xrY860!h1me_PJu2SOexi2Wt!Yif' );

/**#@-*/

/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix = 'wp_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the Codex.
 *
 * @link https://codex.wordpress.org/Debugging_in_WordPress
 */
define( 'WP_DEBUG', false );

/* That's all, stop editing! Happy publishing. */

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) ) {
	define( 'ABSPATH', dirname( __FILE__ ) . '/' );
}

/** Sets up WordPress vars and included files. */
require_once( ABSPATH . 'wp-settings.php' );
