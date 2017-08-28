(function ($, Backbone, _, app) {
    var AppRouter = Backbone.Router.extend({
        // define routers
        routes: {
            '': 'home'
        },
        initialize: function (options) {
            this.contentElement = '#content';
            this.current = null;
            this.header = new app.views.HeaderView();
            // added to the start of the <body>
            $('body').prepend(this.header.el);
            this.header.render();
            Backbone.history.start();
        },
        home: function () {
            var view = new app.views.HomepageView({el: this.contentElement});
            this.render(view);
        },
        route: function (route, name, callback) {
            // Override default route to enforce login on every page
            var login;
            callback = callback || this[name];
            // _.wrap(function, wrapper)
            // 将第一个函数 function 封装到函数wrapper里面, 并把函数 function 作为第一个参数传给wrapper.
            // 这样可以让 wrapper 在 function 运行之前和之后 执行代码, 调整参数然后附有条件地执行.
            callback = _.wrap(callback, function (original) {
                // _.without(array, *values)
                // 返回一个删除所有values值后的array副本
                // TODO: arguments?
                var args = _.without(arguments, original);
                if (app.session.authenticated()) {
                    original.apply(this, args);
                } else {
                    // Show the login screen before calling the view
                    $(this.contentElement).hide();
                    // Bind original callback once the login is successful
                    login = new app.views.LoginView();
                    $(this.contentElement).after(login.el);
                    // 触发done事件时, 执行函数
                    login.on('done', function () {
                        // When logout is finished, the header is rendered again to reflect the new state
                        this.header.render();
                        $(this.contentElement).show();
                        original.apply(this, args);
                    }, this);
                    // Render the login form
                    login.render();
                }
            });
            // 原始的route调用时会执行修饰过(wrapped)的callback函数
            return Backbone.Router.prototype.route.apply(this, [route, name, callback]);
        },
        render: function (view) {
            if (this.current) {
                this.current.undelegateEvents();
                this.current.$el = $();
                this.current.remove();
            }
            this.current = view;
            this.current.render();
        }
    });

    app.router = AppRouter;

})(jQuery, Backbone, _, app);
