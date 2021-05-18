create DATABASE IF NOT EXISTS mindata;

use mindata;

CREATE OR REPLACE TABLE thoughts (
    th_id int not null auto_increment,
    primary key(th_id),
    create_date int not null,
    create_time int not null,
    importance int,
    data varchar(10000) not null,
    calendar_id int DEFAULT 0 not null ,
    catg_id int DEFAULT 0 not null, 
    owner int DEFAULT 0 not null  

);

#Numenclature category names->id
CREATE OR REPLACE TABLE catg_names (
    catg_id int not null, #link to catg 
    catg_name varchar(100) #category desc 
);

#one to many
CREATE OR REPLACE TABLE catg (
    catg_id int not null, #link to catg_names.catg_id
    th_id int not null    #link to thoughts.catg_id 
);

#one to many
CREATE OR REPLACE TABLE calendar (
    th_id int,  # link to thouhgts.calendar_id  
    star_date_rem int, # starting date for reminder 
    end_date_rem int,  # ending date for reminder
    freq varchar(15), # hourly, daily, monthly yearly
    rem_hour int      # when to start reminder
);

CREATE OR REPLACE TABLE users (
    user_id int not null,
    pass varchar( 1000), 
    user_info varchar( 1000), 
    user_role_id int not null #link to roles.role_id future dev
);

##one to many
#CREATE OR REPLACE TABLE roles (
#    user_id int not null,
#    role_id int not null # link to role_names.role_id
#);
#
##Numenclature 
#CREATE OR REPLACE TABLE role_names (
#    role_id int,
#    role_name varchar(100),
#    action_allow int, #link to actions
#    action_disa int,  #link to actuions
#);

