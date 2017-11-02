### 项目说明

#### 环境

Centos6.8        LAMP           Django1.11         MySQL5.8        Python3.6

#### 后台

1. 会员管理：添加（密码和用户名验证），浏览（分页），删除（删除后留在本页），修改（默认选中状态，密码和用户验证）
2. 商品类别管理（共三级）：添加不同等级的类别，分页浏览，删除后留在本页（不能删除非空类别），修改（只改类别名称）
3. 商品管理：浏览（分页），添加（直接可以选择第三级类别），编辑（可以上传放大镜图片），删除，可查看评论（可对其进行删除操作）
4. 订单管理：浏览（分页），查看祥情（修改状态，状态不可回溯）


#### 前台

1. 首页：按照点击量排序
2. 列表页：为三级列表，可分类展示
3. 商品详情：详细商品信息，销量，库存根据下单情况改变，可添加评论（只有在登陆后且购买该商品后评论），只能删除自己的评论，放大镜（数据库调用图片）,同类商品推介
4. 会员模块：注册（密码验证），登录，重置密码（验证），修改（查看个人信息）
5. 购物车：增，删，查（显示只属于当前用户的）改（修改数量，数量会受库存限制），清空
6. 未提交的订单：删，清空
7. 确认之前，如果信息错误，可以重新编辑
8. 订单：按照订单显示每个订单，可以查看详情，并且可以修改订单状态（状态不可回溯）
9. 个人中心：显示每种状态订单的个数，且可查看每种状态的订单


