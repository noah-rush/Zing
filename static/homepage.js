
(function (factory) {
    'use strict';
    if (typeof define === 'function' && define.amd) {
        // AMD. Register as an anonymous module.
        define(['jquery'], factory);
    } else {
        // Browser globals
        factory(jQuery);
    }
}(function ($) {
    'use strict';

    var
        utils = (function () {
            return {
                escapeRegExChars: function (value) {
                    return value.replace(/[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]/g, "\\$&");
                },
                createNode: function (containerClass) {
                    var div = document.createElement('div');
                    div.className = containerClass;
                    div.style.position = 'absolute';
                    div.style.display = 'none';
                    return div;
                }
            };
        }()),

        keys = {
            ESC: 27,
            TAB: 9,
            RETURN: 13,
            LEFT: 37,
            UP: 38,
            RIGHT: 39,
            DOWN: 40
        };

    function Autocomplete(el, options) {
        var noop = function () { },
            that = this,
            defaults = {
                autoSelectFirst: false,
                appendTo: 'body',
                serviceUrl: null,
                lookup: null,
                onSelect: null,
                width: 'auto',
                minChars: 1,
                maxHeight: 300,
                deferRequestBy: 0,
                params: {},
                formatResult: Autocomplete.formatResult,
                delimiter: null,
                zIndex: 9999,
                type: 'GET',
                noCache: false,
                onSearchStart: noop,
                onSearchComplete: noop,
                onSearchError: noop,
                containerClass: 'autocomplete-suggestions',
                tabDisabled: false,
                dataType: 'text',
                currentRequest: null,
                triggerSelectOnValidInput: true,
                lookupFilter: function (suggestion, originalQuery, queryLowerCase) {
                    return suggestion.value.toLowerCase().indexOf(queryLowerCase) !== -1;
                },
                paramName: 'query',
                transformResult: function (response) {
                    return typeof response === 'string' ? $.parseJSON(response) : response;
                }
            };

        // Shared variables:
        that.element = el;
        that.el = $(el);
        that.suggestions = [];
        that.badQueries = [];
        that.selectedIndex = -1;
        that.currentValue = that.element.value;
        that.intervalId = 0;
        that.cachedResponse = {};
        that.onChangeInterval = null;
        that.onChange = null;
        that.isLocal = false;
        that.suggestionsContainer = null;
        that.options = $.extend({}, defaults, options);
        that.classes = {
            selected: 'autocomplete-selected',
            suggestion: 'autocomplete-suggestion'
        };
        that.hint = null;
        that.hintValue = '';
        that.selection = null;

        // Initialize and set options:
        that.initialize();
        that.setOptions(options);
    }

    Autocomplete.utils = utils;

    $.Autocomplete = Autocomplete;

    Autocomplete.formatResult = function (suggestion, currentValue) {
        var pattern = '(' + utils.escapeRegExChars(currentValue) + ')';

        return suggestion.value.replace(new RegExp(pattern, 'gi'), '<strong>$1<\/strong>');
    };

    Autocomplete.prototype = {

        killerFn: null,

        initialize: function () {
            var that = this,
                suggestionSelector = '.' + that.classes.suggestion,
                selected = that.classes.selected,
                options = that.options,
                container;

            // Remove autocomplete attribute to prevent native suggestions:
            that.element.setAttribute('autocomplete', 'off');

            that.killerFn = function (e) {
                if ($(e.target).closest('.' + that.options.containerClass).length === 0) {
                    that.killSuggestions();
                    that.disableKillerFn();
                }
            };

            that.suggestionsContainer = Autocomplete.utils.createNode(options.containerClass);

            container = $(that.suggestionsContainer);

            container.appendTo(options.appendTo);

            // Only set width if it was provided:
            if (options.width !== 'auto') {
                container.width(options.width);
            }

            // Listen for mouse over event on suggestions list:
            container.on('mouseover.autocomplete', suggestionSelector, function () {
                that.activate($(this).data('index'));
            });

            // Deselect active element when mouse leaves suggestions container:
            container.on('mouseout.autocomplete', function () {
                that.selectedIndex = -1;
                container.children('.' + selected).removeClass(selected);
            });

            // Listen for click event on suggestions list:
            container.on('click.autocomplete', suggestionSelector, function () {
                that.select($(this).data('index'));
            });

            that.fixPosition();

            that.fixPositionCapture = function () {
                if (that.visible) {
                    that.fixPosition();
                }
            };

            $(window).on('resize.autocomplete', that.fixPositionCapture);

            that.el.on('keydown.autocomplete', function (e) { that.onKeyPress(e); });
            that.el.on('keyup.autocomplete', function (e) { that.onKeyUp(e); });
            that.el.on('blur.autocomplete', function () { that.onBlur(); });
            that.el.on('focus.autocomplete', function () { that.onFocus(); });
            that.el.on('change.autocomplete', function (e) { that.onKeyUp(e); });
        },

        onFocus: function () {
            var that = this;
            that.fixPosition();
            if (that.options.minChars <= that.el.val().length) {
                that.onValueChange();
            }
        },

        onBlur: function () {
            this.enableKillerFn();
        },

        setOptions: function (suppliedOptions) {
            var that = this,
                options = that.options;

            $.extend(options, suppliedOptions);

            that.isLocal = $.isArray(options.lookup);

            if (that.isLocal) {
                options.lookup = that.verifySuggestionsFormat(options.lookup);
            }

            // Adjust height, width and z-index:
            $(that.suggestionsContainer).css({
                'max-height': options.maxHeight + 'px',
                'width': options.width + 'px',
                'z-index': options.zIndex
            });
        },

        clearCache: function () {
            this.cachedResponse = {};
            this.badQueries = [];
        },

        clear: function () {
            this.clearCache();
            this.currentValue = '';
            this.suggestions = [];
        },

        disable: function () {
            var that = this;
            that.disabled = true;
            if (that.currentRequest) {
                that.currentRequest.abort();
            }
        },

        enable: function () {
            this.disabled = false;
        },

        fixPosition: function () {
            var that = this,
                offset,
                styles;

            // Don't adjsut position if custom container has been specified:
            if (that.options.appendTo !== 'body') {
                return;
            }

            offset = that.el.offset();

            styles = {
                top: (offset.top + that.el.outerHeight()) + 'px',
                left: offset.left + 'px'
            };

            if (that.options.width === 'auto') {
                styles.width = (that.el.outerWidth() - 2) + 'px';
            }

            $(that.suggestionsContainer).css(styles);
        },

        enableKillerFn: function () {
            var that = this;
            $(document).on('click.autocomplete', that.killerFn);
        },

        disableKillerFn: function () {
            var that = this;
            $(document).off('click.autocomplete', that.killerFn);
        },

        killSuggestions: function () {
            var that = this;
            that.stopKillSuggestions();
            that.intervalId = window.setInterval(function () {
                that.hide();
                that.stopKillSuggestions();
            }, 50);
        },

        stopKillSuggestions: function () {
            window.clearInterval(this.intervalId);
        },

        isCursorAtEnd: function () {
            var that = this,
                valLength = that.el.val().length,
                selectionStart = that.element.selectionStart,
                range;

            if (typeof selectionStart === 'number') {
                return selectionStart === valLength;
            }
            if (document.selection) {
                range = document.selection.createRange();
                range.moveStart('character', -valLength);
                return valLength === range.text.length;
            }
            return true;
        },

        onKeyPress: function (e) {
            var that = this;

            // If suggestions are hidden and user presses arrow down, display suggestions:
            if (!that.disabled && !that.visible && e.which === keys.DOWN && that.currentValue) {
                that.suggest();
                return;
            }

            if (that.disabled || !that.visible) {
                return;
            }

            switch (e.which) {
                case keys.ESC:
                    that.el.val(that.currentValue);
                    that.hide();
                    break;
                case keys.RIGHT:
                    if (that.hint && that.options.onHint && that.isCursorAtEnd()) {
                        that.selectHint();
                        break;
                    }
                    return;
                case keys.TAB:
                    if (that.hint && that.options.onHint) {
                        that.selectHint();
                        return;
                    }
                    // Fall through to RETURN
                case keys.RETURN:
                    if (that.selectedIndex === -1) {
                        that.hide();
                        return;
                    }
                    that.select(that.selectedIndex);
                    if (e.which === keys.TAB && that.options.tabDisabled === false) {
                        return;
                    }
                    break;
                case keys.UP:
                    that.moveUp();
                    break;
                case keys.DOWN:
                    that.moveDown();
                    break;
                default:
                    return;
            }

            // Cancel event if function did not return:
            e.stopImmediatePropagation();
            e.preventDefault();
        },

        onKeyUp: function (e) {
            var that = this;

            if (that.disabled) {
                return;
            }

            switch (e.which) {
                case keys.UP:
                case keys.DOWN:
                    return;
            }

            clearInterval(that.onChangeInterval);

            if (that.currentValue !== that.el.val()) {
                that.findBestHint();
                if (that.options.deferRequestBy > 0) {
                    // Defer lookup in case when value changes very quickly:
                    that.onChangeInterval = setInterval(function () {
                        that.onValueChange();
                    }, that.options.deferRequestBy);
                } else {
                    that.onValueChange();
                }
            }
        },

        onValueChange: function () {
            var that = this,
                options = that.options,
                value = that.el.val(),
                query = that.getQuery(value),
                index;

            if (that.selection) {
                that.selection = null;
                (options.onInvalidateSelection || $.noop).call(that.element);
            }

            clearInterval(that.onChangeInterval);
            that.currentValue = value;
            that.selectedIndex = -1;

            // Check existing suggestion for the match before proceeding:
            if (options.triggerSelectOnValidInput) {
                index = that.findSuggestionIndex(query);
                if (index !== -1) {
                    that.select(index);
                    return;
                }
            }

            if (query.length < options.minChars) {
                that.hide();
            } else {
                that.getSuggestions(query);
            }
        },

        findSuggestionIndex: function (query) {
            var that = this,
                index = -1,
                queryLowerCase = query.toLowerCase();

            $.each(that.suggestions, function (i, suggestion) {
                if (suggestion.value.toLowerCase() === queryLowerCase) {
                    index = i;
                    return false;
                }
            });

            return index;
        },

        getQuery: function (value) {
            var delimiter = this.options.delimiter,
                parts;

            if (!delimiter) {
                return value;
            }
            parts = value.split(delimiter);
            return $.trim(parts[parts.length - 1]);
        },

        getSuggestionsLocal: function (query) {
            var that = this,
                options = that.options,
                queryLowerCase = query.toLowerCase(),
                filter = options.lookupFilter,
                limit = parseInt(options.lookupLimit, 10),
                data;

            data = {
                suggestions: $.grep(options.lookup, function (suggestion) {
                    return filter(suggestion, query, queryLowerCase);
                })
            };

            if (limit && data.suggestions.length > limit) {
                data.suggestions = data.suggestions.slice(0, limit);
            }

            return data;
        },

        getSuggestions: function (q) {
            var response,
                that = this,
                options = that.options,
                serviceUrl = options.serviceUrl,
                data,
                cacheKey;

            options.params[options.paramName] = q;
            data = options.ignoreParams ? null : options.params;

            if (that.isLocal) {
                response = that.getSuggestionsLocal(q);
            } else {
                if ($.isFunction(serviceUrl)) {
                    serviceUrl = serviceUrl.call(that.element, q);
                }
                cacheKey = serviceUrl + '?' + $.param(data || {});
                response = that.cachedResponse[cacheKey];
            }

            if (response && $.isArray(response.suggestions)) {
                that.suggestions = response.suggestions;
                that.suggest();
            } else if (!that.isBadQuery(q)) {
                if (options.onSearchStart.call(that.element, options.params) === false) {
                    return;
                }
                if (that.currentRequest) {
                    that.currentRequest.abort();
                }
                that.currentRequest = $.ajax({
                    url: serviceUrl,
                    data: data,
                    type: options.type,
                    dataType: options.dataType
                }).done(function (data) {
                    that.currentRequest = null;
                    that.processResponse(data, q, cacheKey);
                    options.onSearchComplete.call(that.element, q);
                }).fail(function (jqXHR, textStatus, errorThrown) {
                    options.onSearchError.call(that.element, q, jqXHR, textStatus, errorThrown);
                });
            }
        },

        isBadQuery: function (q) {
            var badQueries = this.badQueries,
                i = badQueries.length;

            while (i--) {
                if (q.indexOf(badQueries[i]) === 0) {
                    return true;
                }
            }

            return false;
        },

        hide: function () {
            var that = this;
            that.visible = false;
            that.selectedIndex = -1;
            $(that.suggestionsContainer).hide();
            that.signalHint(null);
        },

        suggest: function () {
            if (this.suggestions.length === 0) {
                this.hide();
                return;
            }

            var that = this,
                options = that.options,
                formatResult = options.formatResult,
                value = that.getQuery(that.currentValue),
                className = that.classes.suggestion,
                classSelected = that.classes.selected,
                container = $(that.suggestionsContainer),
                beforeRender = options.beforeRender,
                html = '',
                index,
                width;

            if (options.triggerSelectOnValidInput) {
                index = that.findSuggestionIndex(value);
                if (index !== -1) {
                    that.select(index);
                    return;
                }
            }

            // Build suggestions inner HTML:
            $.each(that.suggestions, function (i, suggestion) {
                html += '<div class="' + className + '" data-index="' + i + '">' + formatResult(suggestion, value) + '</div>';
            });

            // If width is auto, adjust width before displaying suggestions,
            // because if instance was created before input had width, it will be zero.
            // Also it adjusts if input width has changed.
            // -2px to account for suggestions border.
            if (options.width === 'auto') {
                width = that.el.outerWidth() - 2;
                container.width(width > 0 ? width : 300);
            }

            container.html(html);

            // Select first value by default:
            if (options.autoSelectFirst) {
                that.selectedIndex = 0;
                container.children().first().addClass(classSelected);
            }

            if ($.isFunction(beforeRender)) {
                beforeRender.call(that.element, container);
            }

            container.show();
            that.visible = true;

            that.findBestHint();
        },

        findBestHint: function () {
            var that = this,
                value = that.el.val().toLowerCase(),
                bestMatch = null;

            if (!value) {
                return;
            }

            $.each(that.suggestions, function (i, suggestion) {
                var foundMatch = suggestion.value.toLowerCase().indexOf(value) === 0;
                if (foundMatch) {
                    bestMatch = suggestion;
                }
                return !foundMatch;
            });

            that.signalHint(bestMatch);
        },

        signalHint: function (suggestion) {
            var hintValue = '',
                that = this;
            if (suggestion) {
                hintValue = that.currentValue + suggestion.value.substr(that.currentValue.length);
            }
            if (that.hintValue !== hintValue) {
                that.hintValue = hintValue;
                that.hint = suggestion;
                (this.options.onHint || $.noop)(hintValue);
            }
        },

        verifySuggestionsFormat: function (suggestions) {
            // If suggestions is string array, convert them to supported format:
            if (suggestions.length && typeof suggestions[0] === 'string') {
                return $.map(suggestions, function (value) {
                    return { value: value, data: null };
                });
            }

            return suggestions;
        },

        processResponse: function (response, originalQuery, cacheKey) {
            var that = this,
                options = that.options,
                result = options.transformResult(response, originalQuery);

            result.suggestions = that.verifySuggestionsFormat(result.suggestions);

            // Cache results if cache is not disabled:
            if (!options.noCache) {
                that.cachedResponse[cacheKey] = result;
                if (result.suggestions.length === 0) {
                    that.badQueries.push(cacheKey);
                }
            }

            // Return if originalQuery is not matching current query:
            if (originalQuery !== that.getQuery(that.currentValue)) {
                return;
            }

            that.suggestions = result.suggestions;
            that.suggest();
        },

        activate: function (index) {
            var that = this,
                activeItem,
                selected = that.classes.selected,
                container = $(that.suggestionsContainer),
                children = container.children();

            container.children('.' + selected).removeClass(selected);

            that.selectedIndex = index;

            if (that.selectedIndex !== -1 && children.length > that.selectedIndex) {
                activeItem = children.get(that.selectedIndex);
                $(activeItem).addClass(selected);
                return activeItem;
            }

            return null;
        },

        selectHint: function () {
            var that = this,
                i = $.inArray(that.hint, that.suggestions);

            that.select(i);
        },

        select: function (i) {
            var that = this;
            that.hide();
            that.onSelect(i);
        },

        moveUp: function () {
            var that = this;

            if (that.selectedIndex === -1) {
                return;
            }

            if (that.selectedIndex === 0) {
                $(that.suggestionsContainer).children().first().removeClass(that.classes.selected);
                that.selectedIndex = -1;
                that.el.val(that.currentValue);
                that.findBestHint();
                return;
            }

            that.adjustScroll(that.selectedIndex - 1);
        },

        moveDown: function () {
            var that = this;

            if (that.selectedIndex === (that.suggestions.length - 1)) {
                return;
            }

            that.adjustScroll(that.selectedIndex + 1);
        },

        adjustScroll: function (index) {
            var that = this,
                activeItem = that.activate(index),
                offsetTop,
                upperBound,
                lowerBound,
                heightDelta = 25;

            if (!activeItem) {
                return;
            }

            offsetTop = activeItem.offsetTop;
            upperBound = $(that.suggestionsContainer).scrollTop();
            lowerBound = upperBound + that.options.maxHeight - heightDelta;

            if (offsetTop < upperBound) {
                $(that.suggestionsContainer).scrollTop(offsetTop);
            } else if (offsetTop > lowerBound) {
                $(that.suggestionsContainer).scrollTop(offsetTop - that.options.maxHeight + heightDelta);
            }

            that.el.val(that.getValue(that.suggestions[index].value));
            that.signalHint(null);
        },

        onSelect: function (index) {
            var that = this,
                onSelectCallback = that.options.onSelect,
                suggestion = that.suggestions[index];

            that.currentValue = that.getValue(suggestion.value);
            that.el.val(that.currentValue);
            that.signalHint(null);
            that.suggestions = [];
            that.selection = suggestion;

            if ($.isFunction(onSelectCallback)) {
                onSelectCallback.call(that.element, suggestion);
            }
        },

        getValue: function (value) {
            var that = this,
                delimiter = that.options.delimiter,
                currentValue,
                parts;

            if (!delimiter) {
                return value;
            }

            currentValue = that.currentValue;
            parts = currentValue.split(delimiter);

            if (parts.length === 1) {
                return value;
            }

            return currentValue.substr(0, currentValue.length - parts[parts.length - 1].length) + value;
        },

        dispose: function () {
            var that = this;
            that.el.off('.autocomplete').removeData('autocomplete');
            that.disableKillerFn();
            $(window).off('resize.autocomplete', that.fixPositionCapture);
            $(that.suggestionsContainer).remove();
        }
    };

    // Create chainable jQuery plugin:
    $.fn.autocomplete = function (options, args) {
        var dataKey = 'autocomplete';
        // If function invoked without argument return
        // instance of the first matched element:
        if (arguments.length === 0) {
            return this.first().data(dataKey);
        }

        return this.each(function () {
            var inputElement = $(this),
                instance = inputElement.data(dataKey);

            if (typeof options === 'string') {
                if (instance && typeof instance[options] === 'function') {
                    instance[options](args);
                }
            } else {
                // If instance already exists, destroy it:
                if (instance && instance.dispose) {
                    instance.dispose();
                }
                instance = new Autocomplete(this, options);
                inputElement.data(dataKey, instance);
            }
        });
    };
}));


var stars;

function getnowplaying(){
	$.ajax({
  		url: "/nowPlaying",
		success: displaynowplaying
	});

};
function getzingdescript(){
	$.ajax({
  		url: "/zingDescript",
		success: displayzingdescript
	});

};
function getcomingsoon(){
	$.ajax({
  		url: "/comingsoon",
		success: displaycomingsoon
	});

};
function get_all_shows(){
    $.ajax({
        url: "/allshows",
        success: display_all_shows
    });

};
function full_schedule(){
    $.ajax({
        url: "/fullschedule",
        success: display_full_schedule
    });

};
function display_all_shows(data){
    $("#panelc").find('.panel-body').html(data);
}
function display_full_schedule(data){
    $("#panelc").find('.panel-body').html(data);
}

function profile(){
	$.ajax({
  		url: "/nowPlaying",
		success: displaycomingsoon
	});

};

function autocomp(){
	
	$('#rate').autocomplete({serviceUrl: '/autocomplete/allshows'});
}; 

function facebook(){
	 function statusChangeCallback(response) {
    console.log('statusChangeCallback');
    console.log(response);
    // The response object is returned with a status field that lets the
    // app know the current login status of the person.
    // Full docs on the response object can be found in the documentation
    // for FB.getLoginStatus().
    if (response.status === 'connected') {
      // Logged into your app and Facebook.
      testAPI();
      
    } else if (response.status === 'not_authorized') {
      // The person is logged into Facebook, but not your app.
      
    } else {
      // The person is not logged into Facebook, so we're not sure if
      // they are logged into this app or not.
      

    }
  }

  // This function is called when someone finishes with the Login
  // Button.  See the onlogin handler attached to it in the sample
  // code below.
  function checkLoginState() {
    FB.getLoginStatus(function(response) {
      statusChangeCallback(response);
    });
  }

  window.fbAsyncInit = function() {
  FB.init({
    appId      : 698403073548094,
    cookie     : true,  // enable cookies to allow the server to access 
                        // the session
    xfbml      : true,  // parse social plugins on this page
    version    : 'v2.0' // use version 2.0
  });


  // Now that we've initialized the JavaScript SDK, we call 
  // FB.getLoginStatus().  This function gets the state of the
  // person visiting this page and can return one of three states to
  // the callback you provide.  They can be:
  //
  // 1. Logged into your app ('connected')
  // 2. Logged into Facebook, but not your app ('not_authorized')
  // 3. Not logged into Facebook and can't tell if they are logged into
  //    your app or not.
  //
  // These three cases are handled in the callback function.
FB.getLoginStatus(function(response) {
    statusChangeCallback(response);
  });

  };
  

  // Load the SDK asynchronously
  (function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'));

  // Here we run a very simple test of the Graph API after login is
  // successful.  See statusChangeCallback() for when this call is made.
  function testAPI() {
    console.log('Welcome!  Fetching your information.... ');
    FB.api('/me', function(response) {
      console.log('Successful login for: ' + response.name);
    console.log(JSON.stringify(response));
        var check = $("#panelheaderuser");
        check.html("<div class=\"dropdown\"><button class=\"btn btn-default btn-sm dropdown-toggle\"  type=\"button\" data-toggle=\"dropdown\">\<span class =\"glyphicon glyphicon-user\"></span><span id = \"user\" >  {{useron}}</span>\<span class=\"caret\"></span>\</button><ul class=\"dropdown-menu\" role=\"menu\">\<li><a href=\"#\">Profile</a></li>\ <li><a href=\"#\">Account Settings</a></li>\  <li><a href=\"#logout\">Logout</a></li>\ </ul>\</div>");
        var name = response.first_name;
        console.log(response.first_name);
        name = response.first_name;
        console.log(user);
          $("#user").text(" " + response.first_name + " ");
        $.ajax({
  		url: "/login",
  		success: handle_login,
		data: {
			firstname: response.first_name,
			lastname: response.last_name,
			email: response.email
		}
	});

    });
  }
}

var quickReview = false;

function handle_login(data){
	console.log(data);
}
function displaynowplaying(data){
	
	$("#panelc2").html(data);
}
function displayzingdescript(data){
	
	$("#panelc2").html(data);
}
function displaycomingsoon(data){
	
	$("#panelc3").html(data);
}



function do_stuff() {
	var hiddenBox = $("#blank" );
	var login = $("#submit");
	login.hide();
	var hiddenBox = $("#blank" );
  hiddenBox.hide();

}
function signup(){
	
  var lastname = $("#newlast").val();
	var firstname = $("#newfirst").val();
	var email = $("#newemail").val();
	var password = $("#newpassword").val();
	console.log(lastname, firstname, email, password);
	 $.ajax({
		url: "/facebookcreate",
		data: {
			email:  email,
			firstname: firstname,
			lastname: lastname,
			password: password
		},
		success: show_password
	});
}

function panelMove() {
var panel = $("#panelsignup");
console.log(panel.css("height"));
var px = panel.css("height").indexOf('p')
var number = parseInt(panel.css("height").substring(0, px));
number = number +4;
panel.css("height", number + "px"); // pseudo-property code: Move right by 10px
setTimeout(panelMove,10); // call doMove() in 20 msec
}

function printmonth(){
		console.log("anything")
		//panelMove();
}

function show_signup(data){
		$("#jumbo").html(data);
		//panelMove();
}
function login_rout(data){
	console.log(data);
	var str = data.substring(0,3);
	var somethingwrong = $("#somethingWrong")
	switch(str){
		case "Log":
			var user = data.substring(18);
			console.log(user);
			$("#loginscreen").hide();
			var nouser = $("#nouser");
			nouser.hide();
			var logout = $("#logout");
			var name = $("#name");
			var yesuser = $("#yesuser");
			yesuser.text(user)
			yesuser.show();

			logout.show();
			name.show();
			break;
		case "Use":
			somethingwrong.show();
			somethingwrong.text("Username not found. Try again.");
			window.location.href = "/";
			break;
		case "Inc":
			somethingwrong.show();
			somethingwrong.text("Incorrect Password. Try again.");
			window.location.href = "/";
			break;
		}
}
function logout(){
	var fbresponse = false
	FB.getLoginStatus(function(response) {
     if (response.status === 'connected') {
      // Logged into your app and Facebook.
      fbresponse = true 
      
    }
  });
	if(fbresponse){
	FB.logout(function(response) {
    });
	}
    var check = $("#user");
    check.text(" Login ");
    var check = $("#panelheaderuser");
    check.html( "<a class=\"btn btn-default btn-sm\" href = \"#login\" type=\"button\" ><span class = \"glyphicon glyphicon-user\"></span><span id = \"user\" >  Login</span></a>");
	$.ajax({
  		url: "/logout",
		
	});
}

function login_func(){
	$.ajax({
		success: login_display,
  		url: "/signinform",
		
	});
}
function login_display(data){
	$("#panelc").find('.panel-body').html(data);
}

// function create_Account(){
// 	console.log("got here")
// 	var day = $("#day").val();
// 	var year = $("#year").val();
// 	console.log(year);
// 	console.log(day);
// 	var firstname = $("#first").val();
// 	var lastname = $("#last").val();
// 	var password = $("#password").val();
// 	var passConfirm = $("#confPassword").val();
// 	var email = $("#email").val();
// 	var month = $("#month").val();
// 	$.ajax({
// 		success: show_signup,
//   		url: "/usercreate",
// 		data: {
// 			firstname: firstname,
// 			lastname: lastname,
// 			password: password,
// 			passwordConfirm: passConfirm,
// 			email: email,
// 			month: month,
// 			day: day,
// 			year: year
// 		}
// 	});
// }

function show_venues(){
	$.ajax({
  		url: "/venues",
		success: display_venues
	});
}

function show_nowPlaying(){
	$.ajax({
  		url: "/nowPlaying",
		success: display_nowPlaying
	});
}

function show_reviews(){
	$("#writeuserreview").show();
}

function display_venues(data){
	console.log(data);
	$("#panelc").html(data);
	var iURL = "http://ajax.googleapis.com/ajax/services/search/images";
    $.ajax({
        url: iURL,
        type: 'GET',
        dataType: 'jsonp',
        data: {
            v:  '1.0',
            q:  '',
            format: 'json',
            jsoncallback:  '?'
        },
        success: function(data){
        	json.responseData.results[0].unescapedUrl
            console.log(data);
        },
        error: function(xhr, textStatus, error){
            console.log(xhr.statusText, textStatus, error);
        }
        
    });

};

function display_show(data){
	$("#panelc").find('.panel-body').html(data);
	 var initRating = $("#startRating").text();
 $(".total-star-rating i").css("width", initRating +"%");
 $("input[name='stars']").change(function(){
	stars = this.value;
	console.log(this.value)
});
 $(".good").click(function(){
	console.log(this.value)
});
if(quickReview){
    $('#myModal').modal('show');
};
quickReview = false;
};
function display_venue(data){
	$("#panelc").find('.panel-body').html(data);
	var address = $("#address").text();
	console.log(address)
	var urlsearch = 'https://maps.googleapis.com/maps/api/geocode/json?address=' +address + '&key=AIzaSyAIlo8iZZm7IfAlLbbqPV42jeGHxanPgyg'
	  $.ajax({
  	url: urlsearch,
  	success: initialize
  })

}

var map
 function initialize(data) {
    var map_canvas = document.getElementById('map_canvas');
    var lat = data.results[0]['geometry']['location']['lat'];
	var lng = data.results[0]['geometry']['location']['lng'];
    var map_options = {
      center: new google.maps.LatLng(lat, lng),
      zoom: 16,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    map = new google.maps.Map(map_canvas, map_options);
    var myLatlng = new google.maps.LatLng(lat,lng);
   var marker = new google.maps.Marker({
    position: myLatlng,
    map: map,
    title: $("#showname").text()
});
   var contentString = '<div id="content">'+
      '<div id="siteNotice">'+
      '</div>'+
      '<h1 style = "font-size: 14pt" id="firstHeading" class="firstHeading">' +$("#showname").text() + '</h1>'+
      '<div id="bodyContent">'+
      '</div>'+
      '</div>';

  var infowindow = new google.maps.InfoWindow({
      content: contentString
  });
   google.maps.event.addListener(marker, 'click', function() {
    infowindow.open(map,marker);
  });
	marker.setIcon('http://maps.google.com/mapfiles/ms/icons/green-dot.png')
   marker.setMap(map);
  
   $.ajax({
   	url: "/yelp",
   	data: {
   		lat: lat,
   		lng: lng
   	},
   	success: yelpresults


  })
}

function yelpresults(data){
	data = jQuery.parseJSON(data);

	for(i=0; i<data.length; i++){
		data[i];
		console.log(data[i]);
		var myLatlng = new google.maps.LatLng(data[i][1],data[i][2]);
	var marker = new google.maps.Marker({
    position: myLatlng,
    map: map,
    title:data[i][0]
});
	var contentString = '<div id="content">'+
      '<div id="siteNotice">'+
      '</div>'+
      '<h1 style = "font-size: 14pt" id="firstHeading" class="firstHeading">' +data[i][0] + '</h1>'+
      '<div id="bodyContent">'+
      '</div>'+
      '</div>';

  var infowindow = new google.maps.InfoWindow({
      content: contentString
  });
   google.maps.event.addListener(marker, 'click', function() {
    infowindow.open(map,marker);
  });
	marker.setMap(map);
}
}
function find(){
    data = $('#rate').val();
    console.log(data);
    $.ajax({
        url: '/show',
        data: {
            show: data
        },
        success: display_show
    })
}

function show(data){
	$.ajax({
		url: '/show',
		data: {
			show: data
		},
		success: display_show
	})
};
function venue(data){
	$.ajax({
		url: '/venue',
		data: {
			venue: data
		},
		success: display_venue
	})
};
function show_reviews(){
	$("#writeuserreview").show();
	$("#submitreview").show();
	
}


function display_nowPlaying(data){
	
	$("#venuel").html(data);
};
function facebookLogin(){
	 FB.login(function(response) {
   console.log(response);
   console.log(response.email);
FB.api('/me', function(response) {
	name = response.first_name;
      $.ajax({
   		success: show_password,
		url: "/facebookcreateform",
		data: {
			email:  response.email,
			firstname: response.first_name,
			lastname: response.last_name
		}
	});
  })
  
 }, {scope: 'public_profile,email'});
}
function homepage(){
	$.ajax({
		success: show_container,
		url:"/home"
	})
}

function inputs(){
    $("input[name='topbuttons']").change(function() {
    console.log($('input[name="topbuttons"]:checked').val());
    $("input[name='topbuttons']").each(function(){
    if(this.checked) {
    lastchecked.checked = false;
    console.log($("input[name='topbuttons']:checked").val());
     $("#leftBoxTitle").text($("input[name='topbuttons']:checked").val());
    var but = $( "input[name='topbuttons']:checked").closest("label");
    but.css("background-color", "red");
    lastchecked.css("background-color", "white");
    lastchecked = but;
    }
    
    

})
});
};
function show_container(data){
	$("#panelc").find('.panel-body').html(data);
}

function show_password(data){
	$("#panelc").find('.panel-body').html(data);
	if(data.indexOf("placeholder=\"Password\"")==-1){
		  var check = $("#panelheaderuser");
        check.html("<div class=\"dropdown\"><button class=\"btn btn-default btn-sm dropdown-toggle\"  type=\"button\" data-toggle=\"dropdown\">\<span class =\"glyphicon glyphicon-user\"></span><span id = \"user\" >  {{useron}}</span>\<span class=\"caret\"></span>\</button><ul class=\"dropdown-menu\" role=\"menu\">\<li><a href=\"#\">Profile</a></li>\ <li><a href=\"#\">Account Settings</a></li>\  <li><a href=\"#logout\">Logout</a></li>\ </ul>\</div>");
        
          $("#user").text(" " + name + " ");
	}
}
var name
function fbsignup(){
	var lastname = $("#lastname").text();
	var firstname = $("#firstname").text();
	var email = $("#fbemail").val();
	var password = $("#fbpassword").val();
	console.log(lastname, firstname, email, password)

	 $.ajax({
		url: "/facebookcreate",
		data: {
			email:  email,
			firstname: firstname,
			lastname: lastname,
			password: password
		},
		success: show_password
	});
}


function submit_review(){

	var goods = [];
        $('#checkboxlistgood input:checked').each(function() {
        	console.log(this);
        	goods.push(this.name)
        });
    var bads = [];
        $('#checkboxlistbad input:checked').each(function() {
        	console.log(this);
        	bads.push(this.name)
        });
       
	var text = $("#writeuserreview").val();
	var showname = $("#showname").text();
	console.log(text);
	console.log(stars);
	 $.ajax({
		url: "/submitreview",
		data: {
			show: showname,
			text: text,
			stars: stars,
			goods: JSON.stringify(goods),
			bads: JSON.stringify(bads)
		}
	});
     show(showname);
	  


}

var lastchecked = $("#toprated");

function signin(){
	var email = $("#loginEmail").val();
	var password = $("#loginPassword").val();
	$.ajax({
		url:"/signin",
		data:
		{email:email,
		password:password
		},
		success: show_password
	})
}



function start (){
	getzingdescript();
	//getnowplaying();
	getcomingsoon();
	homepage();
    inputs();


$(window).hashchange( function test(){
	var hash = location.hash;
	if(hash.substring(0,5) == "#show")
	{
		console.log(hash.substring(6));
		show(hash.substring(6));
	}
	if(hash.substring(0,6) == "#venue")
	{
		console.log(hash.substring(7));
		venue(hash.substring(7));
	}
	console.log(hash);
	switch(hash){
	case "#venues":
		show_venues();
		break;
	case "#nowplaying":
		show_nowPlaying();
		break;
	case "#createEvent":
		alert();
		break;
	case "#login":
		login_func();
		break;
	case "#signup":
		signup();
		break;
	case "#fbsignup":
		fbsignup();
		break;
	case "#logout":
		logout();
		break;
	case "#createAccount":
		create_Account();
		break;
	case "#facebookLogin":
		facebookLogin()
		break;
	case "#signin":
		signin()
		break;
	case "#home":
		homepage()
		break;
	case "#profile":
		profile()
		break;
	case "#submitreview":
		submit_review()
		break;
    case "#allshows":
        get_all_shows()
        break;
    case "#fullschedule":
        full_schedule()
        break;




    



	}

});

$("#find").click(function(){
        show($('#rate').val());
       }
       );
$("#modalReview").click(function(){
        show($('#rate').val());
        quickReview = true;
       }
       );





$(window).hashchange();
 $("#submitshowreview").on("click", submit_review);
 console.log('here');
  facebook();
autocomp();
// $("#venues").on("click", show_venues);
// $("#NowPlaying").on( "click", show_nowPlaying);
}
$(document).ready(start);
