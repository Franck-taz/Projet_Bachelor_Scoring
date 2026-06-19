-- Horizon Bank - Database SQL Dump
-- Generated via Django ORM
-- PostgreSQL 18

-- Table: auth_group
CREATE TABLE IF NOT EXISTS "auth_group" (
  "id" integer NOT NULL,
  "name" character varying NOT NULL
);

-- Table: auth_group_permissions
CREATE TABLE IF NOT EXISTS "auth_group_permissions" (
  "id" bigint NOT NULL,
  "group_id" integer NOT NULL,
  "permission_id" integer NOT NULL
);

-- Table: auth_permission
CREATE TABLE IF NOT EXISTS "auth_permission" (
  "id" integer NOT NULL,
  "name" character varying NOT NULL,
  "content_type_id" integer NOT NULL,
  "codename" character varying NOT NULL
);

INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (5, 'Can add permission', 3, 'add_permission');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (6, 'Can change permission', 3, 'change_permission');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (7, 'Can delete permission', 3, 'delete_permission');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (8, 'Can view permission', 3, 'view_permission');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (9, 'Can add group', 2, 'add_group');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (10, 'Can change group', 2, 'change_group');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (11, 'Can delete group', 2, 'delete_group');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (12, 'Can view group', 2, 'view_group');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (13, 'Can add user', 4, 'add_user');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (14, 'Can change user', 4, 'change_user');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (15, 'Can delete user', 4, 'delete_user');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (16, 'Can view user', 4, 'view_user');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (17, 'Can add content type', 5, 'add_contenttype');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (18, 'Can change content type', 5, 'change_contenttype');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (19, 'Can delete content type', 5, 'delete_contenttype');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (20, 'Can view content type', 5, 'view_contenttype');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (21, 'Can add session', 6, 'add_session');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (22, 'Can change session', 6, 'change_session');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (23, 'Can delete session', 6, 'delete_session');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (24, 'Can view session', 6, 'view_session');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (25, 'Can add analyst note', 7, 'add_analystnote');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (26, 'Can change analyst note', 7, 'change_analystnote');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (27, 'Can delete analyst note', 7, 'delete_analystnote');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (28, 'Can view analyst note', 7, 'view_analystnote');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (29, 'Can add loan application', 8, 'add_loanapplication');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (30, 'Can change loan application', 8, 'change_loanapplication');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (31, 'Can delete loan application', 8, 'delete_loanapplication');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (32, 'Can view loan application', 8, 'view_loanapplication');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (33, 'Can add client profile', 10, 'add_clientprofile');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (34, 'Can change client profile', 10, 'change_clientprofile');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (35, 'Can delete client profile', 10, 'delete_clientprofile');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (36, 'Can view client profile', 10, 'view_clientprofile');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (37, 'Can add analyst profile', 9, 'add_analystprofile');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (38, 'Can change analyst profile', 9, 'change_analystprofile');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (39, 'Can delete analyst profile', 9, 'delete_analystprofile');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (40, 'Can view analyst profile', 9, 'view_analystprofile');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (41, 'Can add document', 11, 'add_document');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (42, 'Can change document', 11, 'change_document');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (43, 'Can delete document', 11, 'delete_document');
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES (44, 'Can view document', 11, 'view_document');

-- Table: auth_user
CREATE TABLE IF NOT EXISTS "auth_user" (
  "id" integer NOT NULL,
  "password" character varying NOT NULL,
  "last_login" timestamp with time zone,
  "is_superuser" boolean NOT NULL,
  "username" character varying NOT NULL,
  "first_name" character varying NOT NULL,
  "last_name" character varying NOT NULL,
  "email" character varying NOT NULL,
  "is_staff" boolean NOT NULL,
  "is_active" boolean NOT NULL,
  "date_joined" timestamp with time zone NOT NULL
);

INSERT INTO "auth_user" ("id", "password", "last_login", "is_superuser", "username", "first_name", "last_name", "email", "is_staff", "is_active", "date_joined") VALUES (7, 'pbkdf2_sha256$1200000$98ihOsIckQTnl3wmz569CH$R7B7YXH9ccFWPql3xaPAmDiecsva7qsWfaAJDaGTnFc=', NULL, FALSE, 'bob.smith@gmail.com', 'Bob', 'Smith', 'bob.smith@gmail.com', FALSE, TRUE, 2026-06-19 13:38:02.312618+00:00);
INSERT INTO "auth_user" ("id", "password", "last_login", "is_superuser", "username", "first_name", "last_name", "email", "is_staff", "is_active", "date_joined") VALUES (8, 'pbkdf2_sha256$1200000$ndgeQ116eed62xuPQbFJRg$oktya1pTvDsqWQ4+xIuMlVUmhP1nargEjRcY6ijuaAs=', NULL, FALSE, 'clara.dupont@gmail.com', 'Clara', 'Dupont', 'clara.dupont@gmail.com', FALSE, TRUE, 2026-06-19 13:38:02.527999+00:00);
INSERT INTO "auth_user" ("id", "password", "last_login", "is_superuser", "username", "first_name", "last_name", "email", "is_staff", "is_active", "date_joined") VALUES (9, 'pbkdf2_sha256$1200000$XiKX7FkC8qGWpcrOvaadrj$4r457ABElYs/gAMucVNLz4l+DMESpiMMCiJ6XBuiaHU=', NULL, FALSE, 'david.kumar@gmail.com', 'David', 'Kumar', 'david.kumar@gmail.com', FALSE, TRUE, 2026-06-19 13:38:02.734007+00:00);
INSERT INTO "auth_user" ("id", "password", "last_login", "is_superuser", "username", "first_name", "last_name", "email", "is_staff", "is_active", "date_joined") VALUES (10, 'pbkdf2_sha256$1200000$dzidWjysBHgo8Lez3pd3EG$KKGeYXljNvwB+gLoda8EQpMasfmD/HkpcuHbObSo8ok=', NULL, FALSE, 'emma.wilson@gmail.com', 'Emma', 'Wilson', 'emma.wilson@gmail.com', FALSE, TRUE, 2026-06-19 13:38:02.943919+00:00);
INSERT INTO "auth_user" ("id", "password", "last_login", "is_superuser", "username", "first_name", "last_name", "email", "is_staff", "is_active", "date_joined") VALUES (11, 'pbkdf2_sha256$1200000$jkkGelXta6AR8owjUzpfZz$F/2RC2XbX2Pj9oiJur00YjgM/nUxDt/rHUlDdSpW27E=', NULL, FALSE, 'farid.benali@gmail.com', 'Farid', 'Benali', 'farid.benali@gmail.com', FALSE, TRUE, 2026-06-19 13:38:03.154566+00:00);
INSERT INTO "auth_user" ("id", "password", "last_login", "is_superuser", "username", "first_name", "last_name", "email", "is_staff", "is_active", "date_joined") VALUES (12, 'pbkdf2_sha256$1200000$Lp2YWlrs7ob9tMafDGLtbg$5I+CX1Tgfdcfk3JGTRxpFpgOEglnG0KRfh9v9IIImrg=', NULL, FALSE, 'grace.chen@gmail.com', 'Grace', 'Chen', 'grace.chen@gmail.com', FALSE, TRUE, 2026-06-19 13:38:03.347853+00:00);
INSERT INTO "auth_user" ("id", "password", "last_login", "is_superuser", "username", "first_name", "last_name", "email", "is_staff", "is_active", "date_joined") VALUES (13, 'pbkdf2_sha256$1200000$luq6FU1JQcnXUAKyg8e0tc$emufPTt2uXFyJquaLstIwiUfzCIN/DLQCUWdet0vixw=', NULL, FALSE, 'hugo.rossi@gmail.com', 'Hugo', 'Rossi', 'hugo.rossi@gmail.com', FALSE, TRUE, 2026-06-19 13:38:03.553062+00:00);
INSERT INTO "auth_user" ("id", "password", "last_login", "is_superuser", "username", "first_name", "last_name", "email", "is_staff", "is_active", "date_joined") VALUES (14, 'pbkdf2_sha256$1200000$GQP44F7PVeHJacxs1q5pFl$fKBci/hiLsnC56CR9n7liXcWLRG2ArqadFDl8ojAcQ8=', NULL, FALSE, 'ines.nakamura@gmail.com', 'Ines', 'Nakamura', 'ines.nakamura@gmail.com', FALSE, TRUE, 2026-06-19 13:38:03.783357+00:00);
INSERT INTO "auth_user" ("id", "password", "last_login", "is_superuser", "username", "first_name", "last_name", "email", "is_staff", "is_active", "date_joined") VALUES (6, 'pbkdf2_sha256$1200000$oK0I9ORJa9NxsQVUe1vV7I$l0jiFOwWqvlU/r2pyaFAhbGe14673WW7cfDp3TdqAYY=', 2026-06-19 13:40:43.270670+00:00, FALSE, 'alice.martin@gmail.com', 'Alice', 'Martin', 'alice.martin@gmail.com', FALSE, TRUE, 2026-06-19 13:38:01.960190+00:00);
INSERT INTO "auth_user" ("id", "password", "last_login", "is_superuser", "username", "first_name", "last_name", "email", "is_staff", "is_active", "date_joined") VALUES (5, 'pbkdf2_sha256$1200000$FoCayedgyvQj6CRkoq47mt$xP+C+CiVsCIqgBuHd9/Z1IY2R3W+gMecb2lgLo3WFyo=', 2026-06-19 13:41:36.183921+00:00, TRUE, 'marie-analyst@horizonbank.com', 'Marie', 'Dupont', 'marie-analyst@horizonbank.com', TRUE, TRUE, 2026-06-19 12:53:13.663775+00:00);
INSERT INTO "auth_user" ("id", "password", "last_login", "is_superuser", "username", "first_name", "last_name", "email", "is_staff", "is_active", "date_joined") VALUES (4, 'pbkdf2_sha256$1200000$cAH8qWdSbk9uc26AcDSwXd$Cd/CfEJG1IjZVjg/xzD4IEOxNZZBj7tTQNusdli9+5s=', 2026-06-19 13:11:40.686686+00:00, FALSE, 'johndoe@gmail.com', 'John', 'Doe', 'johndoe@gmail.com', FALSE, TRUE, 2026-06-19 12:53:13.389493+00:00);

-- Table: auth_user_groups
CREATE TABLE IF NOT EXISTS "auth_user_groups" (
  "id" bigint NOT NULL,
  "user_id" integer NOT NULL,
  "group_id" integer NOT NULL
);

-- Table: auth_user_user_permissions
CREATE TABLE IF NOT EXISTS "auth_user_user_permissions" (
  "id" bigint NOT NULL,
  "user_id" integer NOT NULL,
  "permission_id" integer NOT NULL
);

-- Table: django_admin_log
CREATE TABLE IF NOT EXISTS "django_admin_log" (
  "id" integer NOT NULL,
  "action_time" timestamp with time zone NOT NULL,
  "object_id" text,
  "object_repr" character varying NOT NULL,
  "action_flag" smallint NOT NULL,
  "change_message" text NOT NULL,
  "content_type_id" integer,
  "user_id" integer NOT NULL
);

-- Table: django_content_type
CREATE TABLE IF NOT EXISTS "django_content_type" (
  "id" integer NOT NULL,
  "app_label" character varying NOT NULL,
  "model" character varying NOT NULL
);

INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES (1, 'admin', 'logentry');
INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES (2, 'auth', 'group');
INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES (3, 'auth', 'permission');
INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES (4, 'auth', 'user');
INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES (6, 'sessions', 'session');
INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES (7, 'loan_manager', 'analystnote');
INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES (8, 'loan_manager', 'loanapplication');
INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES (9, 'loan_manager', 'analystprofile');
INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES (10, 'loan_manager', 'clientprofile');
INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES (11, 'loan_manager', 'document');

-- Table: django_migrations
CREATE TABLE IF NOT EXISTS "django_migrations" (
  "id" bigint NOT NULL,
  "app" character varying NOT NULL,
  "name" character varying NOT NULL,
  "applied" timestamp with time zone NOT NULL
);

INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (1, 'contenttypes', '0001_initial', 2026-05-23 16:06:48.775735+00:00);
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (2, 'auth', '0001_initial', 2026-05-23 16:06:48.851665+00:00);
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (3, 'admin', '0001_initial', 2026-05-23 16:06:48.874634+00:00);
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (4, 'admin', '0002_logentry_remove_auto_add', 2026-05-23 16:06:48.882021+00:00);
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (5, 'admin', '0003_logentry_add_action_flag_choices', 2026-05-23 16:06:48.888738+00:00);
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (6, 'contenttypes', '0002_remove_content_type_name', 2026-05-23 16:06:48.908138+00:00);
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (7, 'auth', '0002_alter_permission_name_max_length', 2026-05-23 16:06:48.917333+00:00);
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (8, 'auth', '0003_alter_user_email_max_length', 2026-05-23 16:06:48.925230+00:00);
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (9, 'auth', '0004_alter_user_username_opts', 2026-05-23 16:06:48.932254+00:00);
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (10, 'auth', '0005_alter_user_last_login_null', 2026-05-23 16:06:48.941444+00:00);
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (11, 'auth', '0006_require_contenttypes_0002', 2026-05-23 16:06:48.943679+00:00);
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (12, 'auth', '0007_alter_validators_add_error_messages', 2026-05-23 16:06:48.952422+00:00);
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (13, 'auth', '0008_alter_user_username_max_length', 2026-05-23 16:06:48.964844+00:00);
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (14, 'auth', '0009_alter_user_last_name_max_length', 2026-05-23 16:06:48.973298+00:00);
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (15, 'auth', '0010_alter_group_name_max_length', 2026-05-23 16:06:48.984757+00:00);
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (16, 'auth', '0011_update_proxy_permissions', 2026-05-23 16:06:48.992102+00:00);
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (17, 'auth', '0012_alter_user_first_name_max_length', 2026-05-23 16:06:49.001212+00:00);
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (18, 'loan_manager', '0001_initial', 2026-05-23 16:06:49.008394+00:00);
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (19, 'loan_manager', '0002_analystnote_loanapplication_delete_client_and_more', 2026-05-23 16:06:49.062207+00:00);
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (20, 'loan_manager', '0003_alter_loanapplication_house_ownership_and_more', 2026-05-23 16:06:49.079146+00:00);
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (21, 'sessions', '0001_initial', 2026-05-23 16:06:49.098358+00:00);
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (22, 'loan_manager', '0004_analystprofile_clientprofile', 2026-05-25 13:39:10.260916+00:00);
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (23, 'loan_manager', '0005_loanapplication_loan_amount', 2026-05-25 19:20:45.926404+00:00);
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (24, 'loan_manager', '0006_remove_loanapplication_status_and_more', 2026-05-28 18:22:07.713489+00:00);
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (25, 'loan_manager', '0007_analystnote_is_read', 2026-05-29 21:25:54.203801+00:00);
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (26, 'loan_manager', '0008_document', 2026-05-29 21:42:59.885177+00:00);
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES (27, 'loan_manager', '0009_alter_loanapplication_age_and_more', 2026-06-19 12:59:03.938498+00:00);

-- Table: django_session
CREATE TABLE IF NOT EXISTS "django_session" (
  "session_key" character varying NOT NULL,
  "session_data" text NOT NULL,
  "expire_date" timestamp with time zone NOT NULL
);

INSERT INTO "django_session" ("session_key", "session_data", "expire_date") VALUES ('bp0gn6ml0v62iblql9glc3ybmgr3igxp', '.eJxVjEEOwiAQRe_C2hAcaKEu3fcMZAYGqRpISrsy3l1JutDtf-_9l_C4b9nvjVe_RHERgzj9boThwaWDeMdyqzLUsq0Lya7IgzY518jP6-H-HWRsudcWSTmlVFDsQtSMaTIGmBJADOTcWVtKjBDpa46AaE0CHAyMygU9ifcHC6I4qw:1waZTU:kvTUtNTPa3aIzql1u4xyhbse_1XzY1GRZbuCTcug63g', 2026-07-03 13:41:36.187994+00:00);

-- Table: loan_manager_analystnote
CREATE TABLE IF NOT EXISTS "loan_manager_analystnote" (
  "id" bigint NOT NULL,
  "comment" text NOT NULL,
  "created_at" timestamp with time zone NOT NULL,
  "analyst_id" integer,
  "application_id" bigint NOT NULL,
  "is_read" boolean NOT NULL
);

-- Table: loan_manager_analystprofile
CREATE TABLE IF NOT EXISTS "loan_manager_analystprofile" (
  "id" bigint NOT NULL,
  "department" character varying,
  "employee_id" character varying,
  "created_at" timestamp with time zone NOT NULL,
  "user_id" integer NOT NULL
);

-- Table: loan_manager_clientprofile
CREATE TABLE IF NOT EXISTS "loan_manager_clientprofile" (
  "id" bigint NOT NULL,
  "created_at" timestamp with time zone NOT NULL,
  "user_id" integer NOT NULL
);

INSERT INTO "loan_manager_clientprofile" ("id", "created_at", "user_id") VALUES (2, 2026-06-19 12:53:13.659979+00:00, 4);
INSERT INTO "loan_manager_clientprofile" ("id", "created_at", "user_id") VALUES (3, 2026-06-19 13:38:02.279974+00:00, 6);
INSERT INTO "loan_manager_clientprofile" ("id", "created_at", "user_id") VALUES (4, 2026-06-19 13:38:02.515861+00:00, 7);
INSERT INTO "loan_manager_clientprofile" ("id", "created_at", "user_id") VALUES (5, 2026-06-19 13:38:02.722308+00:00, 8);
INSERT INTO "loan_manager_clientprofile" ("id", "created_at", "user_id") VALUES (6, 2026-06-19 13:38:02.933402+00:00, 9);
INSERT INTO "loan_manager_clientprofile" ("id", "created_at", "user_id") VALUES (7, 2026-06-19 13:38:03.144568+00:00, 10);
INSERT INTO "loan_manager_clientprofile" ("id", "created_at", "user_id") VALUES (8, 2026-06-19 13:38:03.336631+00:00, 11);
INSERT INTO "loan_manager_clientprofile" ("id", "created_at", "user_id") VALUES (9, 2026-06-19 13:38:03.541385+00:00, 12);
INSERT INTO "loan_manager_clientprofile" ("id", "created_at", "user_id") VALUES (10, 2026-06-19 13:38:03.768259+00:00, 13);
INSERT INTO "loan_manager_clientprofile" ("id", "created_at", "user_id") VALUES (11, 2026-06-19 13:38:04.005228+00:00, 14);

-- Table: loan_manager_document
CREATE TABLE IF NOT EXISTS "loan_manager_document" (
  "id" bigint NOT NULL,
  "document_type" character varying NOT NULL,
  "file" character varying NOT NULL,
  "uploaded_at" timestamp with time zone NOT NULL,
  "application_id" bigint NOT NULL
);

-- Table: loan_manager_loanapplication
CREATE TABLE IF NOT EXISTS "loan_manager_loanapplication" (
  "id" bigint NOT NULL,
  "age" integer NOT NULL,
  "income" double precision NOT NULL,
  "experience" integer NOT NULL,
  "current_house_yrs" integer NOT NULL,
  "cur_job_years" integer NOT NULL,
  "marital_status" character varying NOT NULL,
  "house_ownership" character varying NOT NULL,
  "car_ownership" character varying NOT NULL,
  "region" character varying NOT NULL,
  "job_category" character varying NOT NULL,
  "risk_score" double precision,
  "risk_flag" integer,
  "created_at" timestamp with time zone NOT NULL,
  "updated_at" timestamp with time zone NOT NULL,
  "user_id" integer NOT NULL,
  "loan_amount" double precision NOT NULL,
  "ai_prediction" character varying,
  "final_decision" character varying
);

INSERT INTO "loan_manager_loanapplication" ("id", "age", "income", "experience", "current_house_yrs", "cur_job_years", "marital_status", "house_ownership", "car_ownership", "region", "job_category", "risk_score", "risk_flag", "created_at", "updated_at", "user_id", "loan_amount", "ai_prediction", "final_decision") VALUES (14, 23, 1303834.0, 3, 13, 3, 'single', 'rented', 'no', 'Central India', 'Engineering', 47.74, 0, 2026-06-19 13:23:48.037867+00:00, 2026-06-19 13:23:48.037876+00:00, 4, 380500.0, 'Pending', NULL);
INSERT INTO "loan_manager_loanapplication" ("id", "age", "income", "experience", "current_house_yrs", "cur_job_years", "marital_status", "house_ownership", "car_ownership", "region", "job_category", "risk_score", "risk_flag", "created_at", "updated_at", "user_id", "loan_amount", "ai_prediction", "final_decision") VALUES (24, 78, 4634680.0, 7, 12, 7, 'single', 'rented', 'no', 'East India', 'Aviation, Defense & Security', 22.72, 0, 2026-06-19 13:38:02.310385+00:00, 2026-06-19 13:38:02.310391+00:00, 6, 1025200.0, 'Approved', NULL);
INSERT INTO "loan_manager_loanapplication" ("id", "age", "income", "experience", "current_house_yrs", "cur_job_years", "marital_status", "house_ownership", "car_ownership", "region", "job_category", "risk_score", "risk_flag", "created_at", "updated_at", "user_id", "loan_amount", "ai_prediction", "final_decision") VALUES (25, 52, 3939397.0, 19, 10, 3, 'single', 'rented', 'yes', 'South India', 'Aviation, Defense & Security', 36.14, 0, 2026-06-19 13:38:02.526478+00:00, 2026-06-19 13:38:02.526484+00:00, 7, 630400.0, 'Pending', NULL);
INSERT INTO "loan_manager_loanapplication" ("id", "age", "income", "experience", "current_house_yrs", "cur_job_years", "marital_status", "house_ownership", "car_ownership", "region", "job_category", "risk_score", "risk_flag", "created_at", "updated_at", "user_id", "loan_amount", "ai_prediction", "final_decision") VALUES (26, 46, 1885923.0, 16, 14, 8, 'single', 'rented', 'no', 'South India', 'Law, Government & Public Service', 73.97, 1, 2026-06-19 13:38:02.732488+00:00, 2026-06-19 13:38:02.732495+00:00, 8, 289800.0, 'Pending', NULL);
INSERT INTO "loan_manager_loanapplication" ("id", "age", "income", "experience", "current_house_yrs", "cur_job_years", "marital_status", "house_ownership", "car_ownership", "region", "job_category", "risk_score", "risk_flag", "created_at", "updated_at", "user_id", "loan_amount", "ai_prediction", "final_decision") VALUES (27, 68, 7839236.0, 7, 14, 7, 'single', 'rented', 'no', 'West India', 'Engineering', 65.93, 1, 2026-06-19 13:38:02.942327+00:00, 2026-06-19 13:38:02.942333+00:00, 9, 1368200.0, 'Pending', NULL);
INSERT INTO "loan_manager_loanapplication" ("id", "age", "income", "experience", "current_house_yrs", "cur_job_years", "marital_status", "house_ownership", "car_ownership", "region", "job_category", "risk_score", "risk_flag", "created_at", "updated_at", "user_id", "loan_amount", "ai_prediction", "final_decision") VALUES (28, 23, 8769550.0, 5, 10, 5, 'single', 'rented', 'no', 'North India', 'Technology & IT', 13.1, 0, 2026-06-19 13:38:03.153335+00:00, 2026-06-19 13:38:03.153341+00:00, 10, 2876100.0, 'Approved', NULL);
INSERT INTO "loan_manager_loanapplication" ("id", "age", "income", "experience", "current_house_yrs", "cur_job_years", "marital_status", "house_ownership", "car_ownership", "region", "job_category", "risk_score", "risk_flag", "created_at", "updated_at", "user_id", "loan_amount", "ai_prediction", "final_decision") VALUES (29, 69, 6694786.0, 17, 11, 11, 'single', 'norent_noown', 'no', 'South India', 'Engineering', 80.17, 1, 2026-06-19 13:38:03.346503+00:00, 2026-06-19 13:38:03.346508+00:00, 11, 1173900.0, 'Rejected', NULL);
INSERT INTO "loan_manager_loanapplication" ("id", "age", "income", "experience", "current_house_yrs", "cur_job_years", "marital_status", "house_ownership", "car_ownership", "region", "job_category", "risk_score", "risk_flag", "created_at", "updated_at", "user_id", "loan_amount", "ai_prediction", "final_decision") VALUES (30, 29, 6715263.0, 0, 11, 0, 'single', 'rented', 'no', 'Central India', 'Engineering', 84.65, 1, 2026-06-19 13:38:03.550997+00:00, 2026-06-19 13:38:03.551006+00:00, 12, 1443200.0, 'Rejected', NULL);
INSERT INTO "loan_manager_loanapplication" ("id", "age", "income", "experience", "current_house_yrs", "cur_job_years", "marital_status", "house_ownership", "car_ownership", "region", "job_category", "risk_score", "risk_flag", "created_at", "updated_at", "user_id", "loan_amount", "ai_prediction", "final_decision") VALUES (31, 35, 9454655.0, 7, 14, 7, 'single', 'rented', 'no', 'South India', 'Law, Government & Public Service', 24.88, 0, 2026-06-19 13:38:03.781307+00:00, 2026-06-19 13:38:03.781315+00:00, 13, 2886400.0, 'Approved', NULL);
INSERT INTO "loan_manager_loanapplication" ("id", "age", "income", "experience", "current_house_yrs", "cur_job_years", "marital_status", "house_ownership", "car_ownership", "region", "job_category", "risk_score", "risk_flag", "created_at", "updated_at", "user_id", "loan_amount", "ai_prediction", "final_decision") VALUES (32, 48, 8600643.0, 17, 13, 6, 'single', 'owned', 'no', 'East India', 'Engineering', 8.4, 0, 2026-06-19 13:38:04.015240+00:00, 2026-06-19 13:38:04.015246+00:00, 14, 2249800.0, 'Approved', NULL);
