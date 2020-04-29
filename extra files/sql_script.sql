create database pharmacy;
create table employees ( e_id int primary key auto_increment,username varchar(40),email varchar(40) unique not null,mobile varchar(10), passwd varchar(300));
create table cocustomer ( c_id int primary key auto_increment,username varchar(40),email varchar(40) unique not null,mobile varchar(10), passwd varchar(300));
create table managers ( username varchar(40),email varchar(40) primary key,mobile varchar(10), passwd varchar(300));
create table products(product_id int primary key,product_name varchar(100) not null,company_name varchar(100) not null,price int not null,threshhold int,stock_present int);
create table manager_order_list( order_id int auto_increment primary key, product_id int not null,quantity int not null ,order_date date, order_status varchar(20),receiving_date date, FOREIGN KEY(product_id) references products(product_id));
create table cocustomer_order_list(c_id int not null,order_id int auto_increment primary key, product_id int not null,quantity int not null, order_date date, order_status varchar(20),receiving_date date, FOREIGN KEY(product_id) references products(product_id),foreign key(c_id) references cocustomer(c_id));
create table stock(product_id int ,order_id int , quantity int ,expiry_date date,columnno int,shelfno varchar(10),FOREIGN KEY(product_id) references products(product_id),FOREIGN KEY(order_id) references manager_order_list(order_id));
create table selling_reports(product_id int ,selling_date date, quantity int, FOREIGN KEY(product_id) references products(product_id));

insert into managers(username,email,mobile,passwd) values("Admin_Name","Manager123@gmail.com","9876543210","$pbkdf2-sha256$29000$JSQkZIyRcq51jnEOQcgZIw$X9.0Ts4SGBR2Q/SbvUssr/KodBV0LbLH5M3yEL65GMQ");

insert into products (product_id , product_name, company_name, price) values 
 (101, 'Combiflam', 'Sanofi India Ldt.', 12),(102, 'Aciloc-150', 'Cadila Ltd.', 23),(103, 'Helkos ', 'Lupin Pharmaceuticals', 15),
 (104, 'Peploc', 'Zydus Cadila Ltd.', 13), (105, 'Ranipep', 'Wockhardt Pharmaceuticals', 60), (106, 'Ranitas', 'Intas Pharmaceuticals Ltd.', 6),
 (107, 'Zynol', 'Micro Labs Ltd.', 34), (108, 'Shelcal', 'Torrent Pharmaceuticals', 90), (109, 'Antoxid-HC', 'Dr. Reddys laboratories Ltd.', 235),
 (110, 'Calcimax Forte', 'Meyer Organics', 224), (111, 'Quogress', 'La Renon Healthcare Pvt Ltd', 592), 
 (112, 'Etoxy-120', 'Mascot Healt Series Ltd.', 189), (113, 'Evah', 'Abott Healthcare Ltd.', 70),
 (114, 'Intacoxia', 'Intas Pharmaceuticals Ltd.', 68), (115, 'Spasmonil', 'Cipla Ltd.', 22), (116, 'Cheston Cold', 'Cipla Ltd.', 44), 
 (117, 'Okacet-L', 'Cipla Ltd.', 57), (118, 'Olox-oz', 'Cipla Ltd.', 95), (119, 'Novamox-250', 'Cipla Ltd.', 106),
 (120, 'Almox-250', 'Alkem Laboratories Ltd.', 70), (121, 'Damoxy-250', 'Alembic Ltd.', 19), (122, 'Mefon-D', 'Shrion Pharmaceuticals', 35),
 (123, 'Gabapentin', 'Sunglow Lifescience Pvt. Ltd.', 388), (124, 'Montek-LC', 'Sun Pharma Laboratories Ltd.', 163),
 (125, 'Montair-LC', 'Cipla Ltd.', 97), (126, 'Lyser D', 'Comed Chemical Ltd.', 194), (127, 'Defcort', 'Macleods Pharmaceuticals Pvt. Ltd.', 112),
 (128, 'Omekinz ', 'Henin Luking Pharma Pvt. Ltd.', 54), (129, 'Evion-400', 'Merck Consumer Healthcare Ltd.', 29), 
 (130, 'Vit-E ', 'Zydus Cadila Ltd.', 24), (131, 'Moxir-CV 625', 'Ravic Healtcare', 116), 
 (132, 'Becosules Capsule', 'Pfizer Ltd.', 38), (133, 'Niofine Forte', 'Klm Laboratories Pvt. Ltd.', 125), 
 (134, 'Saridon', 'Pirmal Enterprises Ltd.', 30), (135, 'Nimusulide', 'Cipla Ltd.', 62), (136, 'Acecloren P', 'Indoco Remedies Ltd.', 58), 
 (137, 'Domstal', 'Torrent Pharmaceuticals', 26), (138, 'Cezvom', 'Novaritis India Ltd.', 33), (139, 'Domped', 'Strides Shasun Ltd.', 90),
 (140, 'Gastractiv', 'Jassen India', 26), (141, 'Stopvom', 'Cadila Ltd.', 25), (142, 'Unistal', 'Unichem Laboratories Ltd.', 104),
 (143, 'Meftal Spas', 'Blue Cross Laboratories Ltd.', 39), (144, 'Calciquick D-3', 'Dr. Morepen Limited', 139), 
 (145, 'Domcet', 'Cipla Ltd.', 48), (146, 'Frankcold', 'Frankiln Healthcare Pvt. Ltd.', 90), (147, 'Nefosar', 'Abbott India Ltd.', 82),
 (148, 'Limcee', 'Abbott Healthcare Pvt. Ltd.', 14), (149, 'Avomine', 'Abbott Healthcare Pvt. Ltd.', 48), (150, 'Emin', 'Cipla Ltd.', 14),
 (151, 'Phenergan', 'Abott Healthcare Ltd.', 31), (152, 'Zental', 'Glaxosmithkline Pharmaceuticals Ltd.', 28),
 (153, 'Lupiworm', 'Lupin Pharmaceuticals', 18), (154, 'Wormal', 'Micro Labs Ltd.', 11), (155, 'Zeebee', 'Ranbaxy Laboratories Ltd.', 18),
 (156, 'Albekem', 'Alkem Laboratories Ltd.', 22);


