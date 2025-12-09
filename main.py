from app import create_app      #导入工厂函数 create_app

app = create_app()              # 创建应用实例


# 启动服务器
if __name__ == '__main__':
    app.run(debug=True)