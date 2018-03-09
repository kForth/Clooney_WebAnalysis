var app = angular.module('app');

app.controller('EventSidebarController', function ($scope, $location, $cookies, $http, $route, AuthService) {
    $scope.isActive = function (viewLocation) {
        return viewLocation.replace("/", "") === $location.path().split('/')[1];
    };

    AuthService.isAuthorized(0).then(function(response){
        console.log(response);
        if(!response.allowed)
            $location.path('/');
        $scope.user_level = response.level;
    });

    $scope.updateEvent = function(){
        var event = $cookies.get('selected-event-id');
        if(event != undefined){
            $http.get('/api/event/' + event + '/update', ['avg']);
        }
    };

    $scope.$parent.leftSidebarVisible = $cookies.get('left-sidebar-visible');
    if($scope.$parent.leftSidebarVisible === undefined) $scope.$parent.leftSidebarVisible = true;

    $scope.$parent.rightSidebarVisible = $cookies.get('right-sidebar-visible');
    if($scope.$parent.rightSidebarVisible === undefined) $scope.$parent.rightSidebarVisible = true;


    $scope.toggleLeftSidebar = function () {
        $scope.$parent.leftSidebarVisible = !$scope.$parent.leftSidebarVisible;
        $cookies.put('left-sidebar-visible', $scope.$parent.leftSidebarVisible);
    };

    $scope.toggleRightSidebar = function () {
        $scope.$parent.rightSidebarVisible = !$scope.$parent.rightSidebarVisible;
        $cookies.put('right-sidebar-visible', $scope.$parent.rightSidebarVisible);
    };

    $scope.getSelectedEvent = function () {
        var event = $cookies.get('selected-event-name');
        if (event === undefined) {
            return 'Select'
        }
        return event;
    };

    $scope.isSelectedEvent = function (event) {
        return event === $cookies.get('selected-event-id');
    };

    $scope.selectEvent = function (event) {
        $cookies.put('selected-event-id', event.id);
        $cookies.put('selected-event-name', event.name);
        $route.reload()
    };

    $scope.match_levels = [
          {
              link: "",
              name: "All Matches"
          },
          {
              link: "qm",
              name: "Qualification"
          },
          {
              link: "qf",
              name: "Quarter-Finals"
          },
          {
              link: "sf",
              name: "Semi-Finals"
          },
          {
              link: "f",
              name: "Finals"
          }
      ];

    $scope.getSelectedLevel = function() {
        if($location.path().split('/')[1] == "m" && $location.path().split('/').length > 2){
            return $location.path().split('/')[2].toUpperCase();
        }
        else{
            return "Select";
        }
    };

    $http.get("/api/events")
        .then(function (response) {
            $scope.events = response.data;
            console.log(response.data);
        });

});



app.controller("PicklistController", function ($scope, $cookies) {
    var cachedList = $cookies.get('picklist');
    if (cachedList != undefined) {
        var picklistArea = angular.element(document.querySelector('#picklist'))[0];
        picklistArea.value = cachedList;
    }

    $scope.updateList = function () {
        var picklistArea = angular.element(document.querySelector('#picklist'))[0];
        $cookies.put('picklist', picklistArea.value);
    };

    $scope.increaseFont = function (event) {
        updateFont(2, event.shiftKey)
    };
    $scope.decreaseFont = function () {
        updateFont(-2, event.shiftKey)
    };
    function updateFont(change, bigChange) {
        if(bigChange) change *= 5;
        var picklistArea = angular.element(document.querySelector('#picklist'))[0];
        if (picklistArea.style.fontSize == '') {
            picklistArea.style.fontSize = 15 + Math.sign(change);
        }
        picklistArea.style.fontSize = parseInt(picklistArea.style.fontSize) + change;
    }

    $scope.saveList = function () {
        var filename = 'picklist.txt';
        var data = angular.element(document.querySelector('#picklist'))[0].value;
        var success = false;
        var contentType = 'text/plain;charset=utf-8';

        try {
            // Try using msSaveBlob if supported
            var blob = new Blob([data], {type: contentType});
            if (navigator.msSaveBlob) {
                navigator.msSaveBlob(blob, filename);
            }
            else {
                // Try using other saveBlob implementations, if available
                var saveBlob = navigator.webkitSaveBlob || navigator.mozSaveBlob || navigator.saveBlob;
                if (saveBlob === undefined) throw "Not supported";
                saveBlob(blob, filename);
            }
            success = true;
        } catch (ex) {
            console.log("saveBlob method failed with the following exception:");
            console.log(ex);
        }

        if (!success) {
            // Get the blob url creator
            var urlCreator = window.URL || window.webkitURL || window.mozURL || window.msURL;
            if (urlCreator) {
                // Try to use a download link
                var link = document.createElement('a');
                if ('download' in link) {
                    // Try to simulate a click
                    try {
                        // Prepare a blob URL
                        var blob = new Blob([data], {type: contentType});
                        var url = urlCreator.createObjectURL(blob);
                        link.setAttribute('href', url);

                        // Set the download attribute (Supported in Chrome 14+ / Firefox 20+)
                        link.setAttribute("download", filename);

                        // Simulate clicking the download link
                        var event = document.createEvent('MouseEvents');
                        event.initMouseEvent('click', true, true, window, 1, 0, 0, 0, 0, false, false, false, false, 0, null);
                        link.dispatchEvent(event);
                        console.log("Download link method with simulated click succeeded");
                        success = true;

                    } catch (ex) {
                        console.log("Download link method with simulated click failed with the following exception:");
                        console.log(ex);
                    }
                }

                if (!success) {
                    // Fallback to window.location method
                    try {
                        // Prepare a blob URL
                        // Use application/octet-stream when using window.location to force download
                        console.log("Trying download link method with window.location ...");
                        var blob = new Blob([data], {type: octetStreamMime});
                        var url = urlCreator.createObjectURL(blob);
                        window.location = url;
                        console.log("Download link method with window.location succeeded");
                        success = true;
                    } catch (ex) {
                        console.log("Download link method with window.location failed with the following exception:");
                        console.log(ex);
                    }
                }

            }
        }

        if (!success) {
            // Fallback to window.open method
            console.log("No methods worked for saving the arraybuffer, using last resort window.open.  Not Implemented");
            //window.open(httpPath, '_blank', '');
        }
    };

    $scope.copyList = function () {
        var textarea = angular.element(document.querySelector('#picklist'))[0];
        textarea.select();
        document.execCommand('copy');
    };

});