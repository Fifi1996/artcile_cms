/*
用户表
编号 账户 密码 注册时间
 */
create table if not exists user(
 id int unsigned not null auto_increment key comment "主键id",
 name varchar(20) not null comment "账户",
 pwd varchar(100) not null comment "密码",
 addtime datetime not null comment "注册时间"
)engine=InnoDB default charset=utf8 comment "会员";

/*
文章表
编号 标题 分类 作者 封面 内容 发布时间
 */
create table if not exists art(
 id int unsigned not null auto_increment key comment "主键id",
 title varchar(100) not null comment "标题",
 cate tinyint unsigned not null comment "分类",
 user_id int unsigned not null comment "作者",
 logo varchar(100) not null comment "封面",
 content mediumtext not null comment "内容"

)engine=InnoDB default charset=utf8 comment "文章";