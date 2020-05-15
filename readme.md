Python Flask订餐系统
=====================
##启动
* export ops_config=local|production && python manage.py runserver

##flask-sqlacodegen

        flask-sqlacodegen 'mysql://root:123456@127.0.0.1/food_db?charset=utf8mb4' --outfile "common/models/model.py"  --flask
        flask-sqlacodegen 'mysql://root:123456@127.0.0.1/food_db?charset=utf8mb4' --tables user --outfile "common/models/user.py"  --flask
