<?xml version="1.0"?>
<mysqldump xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<database name="zscaler_automation">
	<table_structure name="admins">
		<field Field="admin_id" Type="int" Null="NO" Key="PRI" Extra="auto_increment" Comment="" />
		<field Field="kunde_id" Type="int" Null="YES" Key="MUL" Extra="" Comment="" />
		<field Field="email" Type="varchar(100)" Null="NO" Key="UNI" Extra="" Comment="" />
		<field Field="password" Type="varchar(100)" Null="NO" Key="" Extra="" Comment="" />
		<field Field="name" Type="varchar(100)" Null="NO" Key="" Extra="" Comment="" />
		<field Field="surname" Type="varchar(100)" Null="NO" Key="" Extra="" Comment="" />
		<key Table="admins" Non_unique="0" Key_name="PRIMARY" Seq_in_index="1" Column_name="admin_id" Collation="A" Cardinality="0" Null="" Index_type="BTREE" Comment="" Index_comment="" Visible="YES" />
		<key Table="admins" Non_unique="0" Key_name="email" Seq_in_index="1" Column_name="email" Collation="A" Cardinality="0" Null="" Index_type="BTREE" Comment="" Index_comment="" Visible="YES" />
		<key Table="admins" Non_unique="1" Key_name="kunde_id" Seq_in_index="1" Column_name="kunde_id" Collation="A" Cardinality="0" Null="YES" Index_type="BTREE" Comment="" Index_comment="" Visible="YES" />
		<options Name="admins" Engine="InnoDB" Version="10" Row_format="Dynamic" Rows="0" Avg_row_length="0" Data_length="16384" Max_data_length="0" Index_length="32768" Data_free="0" Auto_increment="1" Create_time="2022-07-13 07:41:34" Collation="utf8mb4_0900_ai_ci" Create_options="" Comment="" />
	</table_structure>
	<table_structure name="kunden">
		<field Field="kunde_id" Type="int" Null="NO" Key="PRI" Extra="auto_increment" Comment="" />
		<field Field="name" Type="varchar(256)" Null="NO" Key="" Extra="" Comment="" />
		<field Field="api_key" Type="varchar(100)" Null="NO" Key="UNI" Extra="" Comment="" />
		<field Field="cloud" Type="varchar(100)" Null="NO" Key="" Extra="" Comment="" />
		<field Field="customer_domain" Type="varchar(100)" Null="NO" Key="" Extra="" Comment="" />
		<key Table="kunden" Non_unique="0" Key_name="PRIMARY" Seq_in_index="1" Column_name="kunde_id" Collation="A" Cardinality="0" Null="" Index_type="BTREE" Comment="" Index_comment="" Visible="YES" />
		<key Table="kunden" Non_unique="0" Key_name="api_key" Seq_in_index="1" Column_name="api_key" Collation="A" Cardinality="0" Null="" Index_type="BTREE" Comment="" Index_comment="" Visible="YES" />
		<options Name="kunden" Engine="InnoDB" Version="10" Row_format="Dynamic" Rows="0" Avg_row_length="0" Data_length="16384" Max_data_length="0" Index_length="16384" Data_free="0" Auto_increment="1" Create_time="2022-07-13 07:41:33" Collation="utf8mb4_0900_ai_ci" Create_options="" Comment="" />
	</table_structure>
	<table_structure name="locationgroups">
		<field Field="locgroup_id" Type="int" Null="NO" Key="PRI" Extra="auto_increment" Comment="" />
		<field Field="name" Type="varchar(100)" Null="NO" Key="" Extra="" Comment="" />
		<field Field="typ" Type="varchar(100)" Null="YES" Key="" Extra="" Comment="" />
		<field Field="description" Type="varchar(256)" Null="YES" Key="" Extra="" Comment="" />
		<key Table="locationgroups" Non_unique="0" Key_name="PRIMARY" Seq_in_index="1" Column_name="locgroup_id" Collation="A" Cardinality="0" Null="" Index_type="BTREE" Comment="" Index_comment="" Visible="YES" />
		<options Name="locationgroups" Engine="InnoDB" Version="10" Row_format="Dynamic" Rows="0" Avg_row_length="0" Data_length="16384" Max_data_length="0" Index_length="0" Data_free="0" Auto_increment="1" Create_time="2022-07-13 07:41:33" Collation="utf8mb4_0900_ai_ci" Create_options="" Comment="" />
	</table_structure>
	<table_structure name="locations">
		<field Field="location_id" Type="int" Null="NO" Key="PRI" Extra="auto_increment" Comment="" />
		<field Field="kunde_id" Type="int" Null="YES" Key="MUL" Extra="" Comment="" />
		<field Field="name" Type="varchar(100)" Null="NO" Key="" Extra="" Comment="" />
		<field Field="country" Type="varchar(50)" Null="NO" Key="" Extra="" Comment="" />
		<field Field="tz" Type="varchar(100)" Null="NO" Key="" Extra="" Comment="" />
		<field Field="vpn_creds_id" Type="int" Null="NO" Key="" Extra="" Comment="" />
		<field Field="vpn_creds_type" Type="varchar(100)" Null="NO" Key="" Extra="" Comment="" />
		<field Field="ofwEnabled" Type="tinyint(1)" Null="YES" Key="" Extra="" Comment="" />
		<field Field="ipsControl" Type="tinyint(1)" Null="YES" Key="" Extra="" Comment="" />
		<field Field="authRequired" Type="tinyint(1)" Null="YES" Key="" Extra="" Comment="" />
		<field Field="xffForwardEnabled" Type="tinyint(1)" Null="YES" Key="" Extra="" Comment="" />
		<field Field="profile" Type="varchar(100)" Null="YES" Key="" Extra="" Comment="" />
		<field Field="description" Type="varchar(256)" Null="YES" Key="" Extra="" Comment="" />
		<key Table="locations" Non_unique="0" Key_name="PRIMARY" Seq_in_index="1" Column_name="location_id" Collation="A" Cardinality="0" Null="" Index_type="BTREE" Comment="" Index_comment="" Visible="YES" />
		<key Table="locations" Non_unique="1" Key_name="kunde_id" Seq_in_index="1" Column_name="kunde_id" Collation="A" Cardinality="0" Null="YES" Index_type="BTREE" Comment="" Index_comment="" Visible="YES" />
		<options Name="locations" Engine="InnoDB" Version="10" Row_format="Dynamic" Rows="0" Avg_row_length="0" Data_length="16384" Max_data_length="0" Index_length="16384" Data_free="0" Auto_increment="1" Create_time="2022-07-13 07:41:34" Collation="utf8mb4_0900_ai_ci" Create_options="" Comment="" />
	</table_structure>
	<table_structure name="mapp_loc_locgroups">
		<field Field="locgroup_id" Type="int" Null="YES" Key="MUL" Extra="" Comment="" />
		<field Field="location_id" Type="int" Null="YES" Key="MUL" Extra="" Comment="" />
		<key Table="mapp_loc_locgroups" Non_unique="1" Key_name="locgroup_id" Seq_in_index="1" Column_name="locgroup_id" Collation="A" Cardinality="0" Null="YES" Index_type="BTREE" Comment="" Index_comment="" Visible="YES" />
		<key Table="mapp_loc_locgroups" Non_unique="1" Key_name="location_id" Seq_in_index="1" Column_name="location_id" Collation="A" Cardinality="0" Null="YES" Index_type="BTREE" Comment="" Index_comment="" Visible="YES" />
		<options Name="mapp_loc_locgroups" Engine="InnoDB" Version="10" Row_format="Dynamic" Rows="0" Avg_row_length="0" Data_length="16384" Max_data_length="0" Index_length="32768" Data_free="0" Create_time="2022-07-13 07:41:34" Collation="utf8mb4_0900_ai_ci" Create_options="" Comment="" />
	</table_structure>
	<table_structure name="mapp_loc_sublocgroups">
		<field Field="locgroup_id" Type="int" Null="YES" Key="MUL" Extra="" Comment="" />
		<field Field="sublocation_id" Type="int" Null="YES" Key="MUL" Extra="" Comment="" />
		<key Table="mapp_loc_sublocgroups" Non_unique="1" Key_name="locgroup_id" Seq_in_index="1" Column_name="locgroup_id" Collation="A" Cardinality="0" Null="YES" Index_type="BTREE" Comment="" Index_comment="" Visible="YES" />
		<key Table="mapp_loc_sublocgroups" Non_unique="1" Key_name="sublocation_id" Seq_in_index="1" Column_name="sublocation_id" Collation="A" Cardinality="0" Null="YES" Index_type="BTREE" Comment="" Index_comment="" Visible="YES" />
		<options Name="mapp_loc_sublocgroups" Engine="InnoDB" Version="10" Row_format="Dynamic" Rows="0" Avg_row_length="0" Data_length="16384" Max_data_length="0" Index_length="32768" Data_free="0" Create_time="2022-07-13 07:41:34" Collation="utf8mb4_0900_ai_ci" Create_options="" Comment="" />
	</table_structure>
	<table_structure name="projects">
		<field Field="user_id" Type="int" Null="YES" Key="MUL" Extra="" Comment="" />
		<field Field="kunde_id" Type="int" Null="YES" Key="MUL" Extra="" Comment="" />
		<key Table="projects" Non_unique="1" Key_name="user_id" Seq_in_index="1" Column_name="user_id" Collation="A" Cardinality="0" Null="YES" Index_type="BTREE" Comment="" Index_comment="" Visible="YES" />
		<key Table="projects" Non_unique="1" Key_name="kunde_id" Seq_in_index="1" Column_name="kunde_id" Collation="A" Cardinality="0" Null="YES" Index_type="BTREE" Comment="" Index_comment="" Visible="YES" />
		<options Name="projects" Engine="InnoDB" Version="10" Row_format="Dynamic" Rows="0" Avg_row_length="0" Data_length="16384" Max_data_length="0" Index_length="32768" Data_free="0" Create_time="2022-07-13 07:41:33" Collation="utf8mb4_0900_ai_ci" Create_options="" Comment="" />
	</table_structure>
	<table_structure name="sublocations">
		<field Field="sublocation_id" Type="int" Null="NO" Key="PRI" Extra="auto_increment" Comment="" />
		<field Field="location_id" Type="int" Null="YES" Key="MUL" Extra="" Comment="" />
		<field Field="name" Type="varchar(100)" Null="NO" Key="" Extra="" Comment="" />
		<field Field="country" Type="varchar(100)" Null="NO" Key="" Extra="" Comment="" />
		<field Field="tz" Type="varchar(100)" Null="NO" Key="" Extra="" Comment="" />
		<field Field="vpn_creds_id" Type="int" Null="NO" Key="" Extra="" Comment="" />
		<field Field="vpn_creds_type" Type="varchar(100)" Null="NO" Key="" Extra="" Comment="" />
		<field Field="ofwEnabled" Type="tinyint(1)" Null="YES" Key="" Extra="" Comment="" />
		<field Field="ipsControl" Type="tinyint(1)" Null="YES" Key="" Extra="" Comment="" />
		<field Field="authRequired" Type="tinyint(1)" Null="YES" Key="" Extra="" Comment="" />
		<field Field="xffForwardEnabled" Type="tinyint(1)" Null="YES" Key="" Extra="" Comment="" />
		<field Field="profile" Type="varchar(100)" Null="YES" Key="" Extra="" Comment="" />
		<field Field="description" Type="varchar(256)" Null="YES" Key="" Extra="" Comment="" />
		<key Table="sublocations" Non_unique="0" Key_name="PRIMARY" Seq_in_index="1" Column_name="sublocation_id" Collation="A" Cardinality="0" Null="" Index_type="BTREE" Comment="" Index_comment="" Visible="YES" />
		<key Table="sublocations" Non_unique="1" Key_name="location_id" Seq_in_index="1" Column_name="location_id" Collation="A" Cardinality="0" Null="YES" Index_type="BTREE" Comment="" Index_comment="" Visible="YES" />
		<options Name="sublocations" Engine="InnoDB" Version="10" Row_format="Dynamic" Rows="0" Avg_row_length="0" Data_length="16384" Max_data_length="0" Index_length="16384" Data_free="0" Auto_increment="1" Create_time="2022-07-13 07:41:34" Collation="utf8mb4_0900_ai_ci" Create_options="" Comment="" />
	</table_structure>
	<table_structure name="users">
		<field Field="user_id" Type="int" Null="NO" Key="PRI" Extra="auto_increment" Comment="" />
		<field Field="email" Type="varchar(100)" Null="NO" Key="UNI" Extra="" Comment="" />
		<field Field="password" Type="varchar(100)" Null="NO" Key="" Extra="" Comment="" />
		<field Field="name" Type="varchar(100)" Null="NO" Key="" Extra="" Comment="" />
		<field Field="surname" Type="varchar(100)" Null="NO" Key="" Extra="" Comment="" />
		<key Table="users" Non_unique="0" Key_name="PRIMARY" Seq_in_index="1" Column_name="user_id" Collation="A" Cardinality="0" Null="" Index_type="BTREE" Comment="" Index_comment="" Visible="YES" />
		<key Table="users" Non_unique="0" Key_name="email" Seq_in_index="1" Column_name="email" Collation="A" Cardinality="0" Null="" Index_type="BTREE" Comment="" Index_comment="" Visible="YES" />
		<options Name="users" Engine="InnoDB" Version="10" Row_format="Dynamic" Rows="0" Avg_row_length="0" Data_length="16384" Max_data_length="0" Index_length="16384" Data_free="0" Auto_increment="1" Create_time="2022-07-13 07:41:33" Collation="utf8mb4_0900_ai_ci" Create_options="" Comment="" />
	</table_structure>
</database>
</mysqldump>
