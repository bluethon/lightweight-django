(function ($, Backbone, _, app) {

    var TemplateView = Backbone.View.extend({
        templateName: '',
        initialize: function () {
            this.template = _.template($(this.templateName).html());
        },
        render: function () {
            var context = this.getContext(),
                html = this.template(context);
            this.$el.html(html);
        },
        getContext: function () {
            return {};
        }
    });

    var FormView = TemplateView.extend({
        events: {
            // 监听(listen)所有 form的submit, 执行submit回调(callback)
            'submit form': 'submit'
        },
        errorTemplate: _.template('<span class="error"><%- msg %></span>'),
        clearErrors: function () {
            $('.error', this.form.remove());
        },
        showErrors: function (errors) {
            // TODO: Show the errors from the response
            // 映射对象obj,         obj.v         obj.k
            _.map(errors, function (fieldErrors, name) {
                var field = $(':input[name=' + name + ']', this.form),
                    label = $('label[for=' + field.attr('id') + ']', this.form);
                if (label.length === 0) {
                    label = $('label', this.form).first();
                }

                function appendError(msg) {
                    label.before(this.errorTemplate({msg: msg}));
                }

                _.map(fieldErrors, appendError, this);      // 循环增加显示的错误html
                // errors本身(context)
            }, this);
        },
        serializeForm: function (form) {
            // _.object, 对象化, 即{}
            return _.object(_.map(form.serializeArray(), function (item) {
                // Convert object to tuple of (name, value)
                return [item.name, item.value];
            }));
        },
        submit: function (event) {
            var data = {};
            // 阻止默认提交, 由view来处理提交和返回
            event.preventDefault();
            this.form = $(event.currentTarget);
            this.clearErrors();
        },
        failure: function (xhr, status, error) {
            var errors = xhr.responseJSON;
            this.showErrors(errors);
        },
        done: function (event) {
            if (event) {
                event.preventDefault();
            }
            // trigger event
            this.trigger('done');
            this.remove();
        }
    });

    var HomepageView = TemplateView.extend({
        templateName: '#home-template'
    });

    var LoginView = TemplateView.extend({
        id: 'login',
        templateName: '#login-template',
        // errorTemplate: _.template('<span class="error"><%- msg %></span>'),
        // events: {
        //     // 监听(listen)所有 form的submit, 执行submit回调(callback)
        //     'submit form': 'submit'
        // },
        submit: function (event) {
            var data = {};

            // // 阻止默认提交, 由view来处理提交和返回
            // event.preventDefault();
            // this.form = $(event.currentTarget);
            // this.clearErrors();
            // data = {
            //     username: $(':input[name="username"]', this.form).val(),
            //     password: $(':input[name="password"]', this.form).val()
            // };
            // js没有super, 但是下面语句等价调用了父方法
            FormView.prototype.submit.apply(this, arguments);
            data = this.serializeForm(this.form);

            $.post(app.apiLogin, data)
            // $.proxy(), 接受一个函数，然后返回一个新函数，并且这个新函数始终保持了特定的上下文语境
                .success($.proxy(this.loginSuccess, this))
                .fail($.proxy(this.failure, this));
        },
        loginSuccess: function (data) {
            app.session.save(data.token);
            // this.trigger('login', data.token);
            this.done();
        }
        // loginFailure: function (xhr, status, error) {
        //     var errors = xhr.responseJSON;
        //     this.showErrors(errors);
        // },
        // showErrors: function (errors) {
        //     // TODO: Show the errors from the response
        //     // 映射对象obj,         obj.v         obj.k
        //     _.map(errors, function (fieldErrors, name) {
        //         var field = $(':input[name=' + name + ']', this.form),
        //             label = $('label[for=' + field.attr('id') + ']', this.form);
        //         if (label.length === 0) {
        //             label = $('label', this.form).first();
        //         }
        //         function appendError(msg) {
        //             label.before(this.errorTemplate({msg: msg}));
        //         }
        //         _.map(fieldErrors, appendError, this);      // 循环增加显示的错误html
        //     // errors本身(context)
        //     }, this);
        // },
        // // 移除form中所有存在的class="error"的元素
        // clearErrors: function () {
        //     $('.error', this.form).remove();
        // }
    });

    // var HomepageView = Backbone.View.extend({
    //     templateName: '#home-template',
    //     initialize: function () {
    //         this.template = _.template($(this.templateName).html());
    //     },
    //     render: function () {
    //         var context = this.getContext(),
    //             html = this.template(context);
    //         this.$el.html(html);
    //     },
    //     getContext: function () {
    //         return {};
    //     }
    // });

    // var LoginView = Backbone.View.extend({
    //     id: 'login',
    //     templateName: '#login-template',
    //     initialize: function () {
    //         this.template = _.template($(this.templateName).html()):
    //     },
    //     render: function () {
    //         var context = this.getContext(),
    //             html = this.template(context);
    //         this.$el.html(html);
    //     },
    //     getContext: function () {
    //         return {};
    //     }
    // });
    var HeaderView = TemplateView.extend({
        // this means the template renders into a <header> element
        tagName: 'header',
        templateName: '#header-template',
        // TODO: ?, 包括书中解释, two link?
        events: {
            'click a.logout': 'logout'
        },
        // The authenticated value is passed to the template context based on the current session state
        // It won't automatically be updated if this state changes
        // The view will have to be rendered again
        getContext: function () {
            return {authenticated: app.session.authenticated()};
        },
        logout: function (event) {
            event.preventDefault();
            app.session.delete();
            window.location = '/';
        }
    });

    app.views.HomepageView = HomepageView;
    app.views.LoginView = LoginView;
    app.views.HeaderView = HeaderView;

})(jQuery, Backbone, _, app);
