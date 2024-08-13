let map;

var map_options = {
    center: {
        lat: 38.755,
        lng: -98.82
    },
    zoom: 4
};

async function initMap() {
  const { Map } = await google.maps.importLibrary("maps");

  map = new Map(document.getElementById("map"), map_options);
}

initMap();




//
//var map;
//var surgeons = [];
//var all_markers = [];
//
//var geocoder;
//
//var search_e = document.getElementById("search");
//var current_search = [];
//
//var info_windows = [];
//var markerClusterer
//
//search_e.addEventListener("keypress", function (e) {
//    if (e.code === "Enter") {
//        if (search_e.value.length > 0)
//            search();
//    }
//});
//
//function latlng_exists(position) {
//    for (i = 0; i < all_markers.length; i++) {
//        var cm = all_markers[i];
//        if (cm.position.equals(position)) {
//            console.log("marker exists")
//            return true;
//        }
//    }
//
//    return false;
//}
//
//function initMap() {
//    map = new google.maps.Map(document.getElementById('map'), mapOptions);
//
//    $.post("/current_surgeons", {}, function (surgeon_data) {
//        surgeons = surgeon_data;
//        surgeons.forEach(surgeon => {
//            var markers = create_markers(surgeon, map)
//            markers.forEach(m => {
//                all_markers.push(m);
//                // if (!latlng_exists(m.position))
//                //     all_markers.push(m)
//                // else
//                //     m.setMap(null);
//                // console.log(`${m.position.lat()}, ${m.position.lng()}`)
//            })
//            // all_markers = all_markers.concat(markers);
//        });
//
//        reset_marker_cluster(all_markers);
//        // center_users_location()
//        geocoder = new google.maps.Geocoder();
//
//        load_current_location();
//    });
//}
//
//var num_fails = 0;
//
//function load_current_location() {
//    $.ajax('http://ip-api.com/json')
//        .then(
//            function success(response) {
//                zipcode = response.zip;
//                $("#search").val(zipcode);
//                search();
//            },
//
//            function fail(data, status) {
//                console.log("Request for current location failed. Retrying");
//                window.setTimeout(function () {
//                    if (num_fails < 3) {
//                        load_current_location()
//                        num_fails++;
//                    }
//                }, 300)
//            }
//        );
//}
//
//function create_surgeon_listing_html(name, latlng, location_title) {
//    var surgeon_listing_html = `
//        <div onclick="show_surgeon(this)" class="row result-surgeon-row">
//            <div class="col-12">
//                <span class="surgeon-title" id='${latlng}'>${name}</span>
//                <span class="location-title">${location_title}</span>
//            </div>
//        </div>
//    `;
//    return surgeon_listing_html;
//}
//
//function create_surgeon_final_listing_html(name, latlng, location_title) {
//    var surgeon_listing_html = `
//        <div onclick="show_surgeon_final(this)" class="row result-surgeon-row">
//            <div class="col-12">
//                <span class="surgeon-title" id='${latlng}'>${name}</span>
//                <span class="location-title">${location_title}</span>
//            </div>
//        </div>
//    `;
//    return surgeon_listing_html;
//}
//
//function show_surgeon_final(element) {
//    var title_element = $(element).find(".surgeon-title");
//    var title = title_element.text();
//    var id = title_element.attr("id");
//    var surgeon = surgeons.filter(s => {
//        return s.title === title && s.latlng === id;
//    })[0];
//
//    if ($(".results-container").find(".fas").hasClass("fa-caret-up"))
//        show_hide_results(null);
//
//    $("#multiple-surgeon-modal").modal('hide');
//    bring_surgeon_to_view(surgeon);
//}
//
//function show_multiple_surgeon_modal(surgeons_same_title) {
//    $("#multiple-surgeon-modal").modal();
//    $(".modal-body").empty();
//
//    surgeons_same_title.forEach(s => {
//        var surgeon_listing_html = create_surgeon_final_listing_html(s.title, s.latlng, '');
//        $(".modal-body").append(surgeon_listing_html)
//    })
//}
//
//function get_surgeons_by_title(title) {
//    return surgeons.filter(s => {
//        return s.title === title;
//    })
//}
//
//function show_surgeon(element) {
//    var title_element = $(element).find(".surgeon-title");
//    var title = title_element.text();
//    var latlng = title_element.attr("id")
//
//    var surgeons_same_title = get_surgeons_by_title(title)
//
//    console.log(surgeons_same_title);
//
//    if (surgeons_same_title.length === 1) {
//        show_hide_results(null);
//        bring_surgeon_to_view(surgeons_same_title[0]);
//
//    } else if (surgeons_same_title.length > 1) {
//        show_surgeons_same_title(title)
//        // show_multiple_surgeon_modal(surgeons_same_title);
//
//    }
//}
//
//function show_surgeons_same_title(title) {
//    var markers = []
//
//    var latlngs_done = [];
//
//    var c_surgeons = [];
//
//    surgeons.forEach(s => {
//        if (s.title === title) {
//            c_surgeons.push(s);
//
//
//        }
//    })
//
//    c_surgeons.forEach(surgeon => {
//        var ll = surgeon.latlng;
//
//        var s_ll = ll.split("|");
//
//        s_ll.forEach(latlng => {
//            if (latlngs_done.indexOf(latlng) === -1) {
//                latlngs_done.push(latlng);
//
//                var latlng_split = latlng.split(",");
//
//                var lat_lng = {
//                    lat: parseFloat(latlng_split[0]),
//                    lng: parseFloat(latlng_split[1])
//                }
//
//                var marker = new google.maps.Marker({
//                    position: lat_lng,
//                    map: map,
//                    title: `${surgeon.title}||${surgeon.latlng}`
//                });
//
//                var surgeon_info_html = create_surgeon_info_html(surgeon);
//
//                marker.addListener('click', function () {
//                    var infowindow = new google.maps.InfoWindow({
//                        content: surgeon_info_html
//                    });
//                    info_windows.push(infowindow)
//                    infowindow.open(map, marker)
//                });
//
//                markers.push(marker);
//            }
//        });
//
//    });
//
//    reset();
//    reset_marker_cluster(markers);
//
//    var bounds = new google.maps.LatLngBounds();
//
//    markers.forEach(m => {
//        var loc = new google.maps.LatLng(m.position.lat(), m.position.lng());
//        bounds.extend(loc);
//    })
//
//    map.fitBounds(bounds);
//    map.panToBounds(bounds);
//}
//
//function bring_surgeon_to_view(surgeon) {
//
//    var latlngs_done = [];
//    var ltlg = surgeon.latlng;
//    var lls = ltlg.split("|");
//
//    var markers = [];
//
//    lls.forEach(latlng => {
//
//        if (latlngs_done.indexOf(latlng) === -1) {
//            latlngs_done.push(latlng);
//
//            var latlng_split = latlng.split(",");
//
//            var lat_lng = {
//                lat: parseFloat(latlng_split[0]),
//                lng: parseFloat(latlng_split[1])
//            }
//
//            var marker = new google.maps.Marker({
//                position: lat_lng,
//                map: map,
//                title: `${surgeon.title}||${surgeon.latlng}`
//            });
//
//            var surgeon_info_html = create_surgeon_info_html(surgeon);
//
//            marker.addListener('click', function () {
//                var infowindow = new google.maps.InfoWindow({
//                    content: surgeon_info_html
//                });
//                info_windows.push(infowindow)
//                infowindow.open(map, marker)
//            });
//
//            markers.push(marker);
//        }
//    });
//
//    reset_marker_cluster(markers);
//
//    var bounds = new google.maps.LatLngBounds();
//
//    markers.forEach(m => {
//        var loc = new google.maps.LatLng(m.position.lat(), m.position.lng());
//        bounds.extend(loc);
//    })
//
//    map.fitBounds(bounds);
//    map.panToBounds(bounds);
//
//    if (markers.length === 1) {
//        map.setZoom(11);
//    }
//
//}
//
//function show_hide_results(element) {
//    var caret = $(".results-container").find('.fas')[0];
//    caret = $(caret);
//
//    if (caret.hasClass("fa-caret-up")) {
//        caret.removeClass("fa-caret-up");
//        caret.addClass("fa-caret-down")
//        $(".result-surgeon-row").hide();
//
//    } else {
//        caret.removeClass("fa-caret-down");
//        caret.addClass("fa-caret-up")
//        $(".result-surgeon-row").show();
//    }
//}
//
//function search_results_title_html(num_results) {
//    var num_search_results = `
//        <div class="row num-results">
//            <div class="col-xs-12">
//                <div onclick="show_hide_results(this)">Found ${num_results} surgeons
//                    <i class="fas fa-lg fa-caret-up"></i>
//
//                </div>
//            </div>
//        </div>
//    `;
//    return num_search_results;
//}
//
//function filter_surgeons(current_surgeons) {
//    var filtered_surgeons = []
//
//    if (current_surgeons.length > 0) {
//        current_surgeons.forEach(s => {
//            if (!surgeon_exists(s, filtered_surgeons)) {
//                filtered_surgeons.push(s);
//            }
//        })
//    }
//
//    return filtered_surgeons;
//}
//
//function title_not_exist(title, surgeons) {
//    for (i = 0; i < surgeons.length; i++) {
//        if (surgeons[i].title === title)
//            return false;
//    }
//
//    return true;
//}
//
//function search() {
//    var search_value = $("#search").val();
//    // console.log("Searching " + search_value)
//
//    if (search_value.length >= 5 && !isNaN(search_value)) {
//
//        reset();
//
//        jQuery.post('/search', { search_value: search_value }, (data) => {
//
//            $(".results-container .container-fluid").empty();
//
//            geocoder.geocode({ 'address': search_value }, function (results, status) {
//                if (status == google.maps.GeocoderStatus.OK) {
//                    result = results[0];
//                    map.setCenter(result.geometry.location);
//                    // console.log(result)
//                    $("#search").val(result.formatted_address);
//                    map.setZoom(10);
//                } else {
//                    console.log("bad search data")
//                }
//            })
//
//        })
//
//    } else {
//        jQuery.post('/search', { search_value: search_value }, (data) => {
//
//            current_search = [];
//
//            $(".results-container .container-fluid").empty();
//
//            data.forEach(surgeon => {
//                if (is_last_name(surgeon.title, search_value)) {
//                    if (title_not_exist(surgeon.title, current_search)) {
//                        console.log(`Adding ${surgeon.title} to current search`)
//                        current_search.push(surgeon);
//                        // var location_title = get_location_title(surgeon.locations);
//                        var surgeon_listing = create_surgeon_listing_html(surgeon.title, surgeon.latlng, '');
//                        $(".results-container .container-fluid").append(surgeon_listing);
//                    }
//                }
//                // if (!surgeon_exists(surgeon, current_search)) {
//                //     if (is_last_name(surgeon.title, search_value)) {
//                //         current_search.push(surgeon);
//                //
//                //     }
//                // }
//            });
//
//            $(".results-container .container-fluid").prepend(search_results_title_html(current_search.length));
//
//            if (current_search.length == 0) {
//
//                if (markerClusterer && markerClusterer.markers_.length === 1)
//                    reset();
//
//                geocoder.geocode({ 'address': search_value }, function (results, status) {
//                    if (status == google.maps.GeocoderStatus.OK) {
//                        result = results[0];
//                        map.setCenter(result.geometry.location);
//                        $("#search").val(result.formatted_address);
//                        map.setZoom(10);
//                    } else {
//
//                    }
//
//                    $(".results-container .container-fluid").empty();
//
//                })
//            }
//        });
//    }
//}
//
//function is_last_name(title, search_value) {
//    var name = title.split(",")[0];
//    var name_args = name.split(" ")
//    var last_name = name_args[name_args.length - 1]
//    return search_value.toLowerCase() === last_name.toLowerCase()
//}
//
//function locations_equal(s1, s2) {
//
//    var i, j;
//    var locations_1 = JSON.parse(s1.locations)
//    var locations_2 = JSON.parse(s2.locations);
//
//    var equal = true;
//
//    for (i = 0; i < locations_1.length; i++) {
//        var current_location = locations_1[i];
//        if (!location_exists(current_location, locations_2)) {
//            equal = false;
//        }
//    }
//
//    return equal;
//}
//
//function location_exists(current_location, locations_2) {
//    for (var j = 0; j < locations_2.length; j++) {
//        var possible_match = locations_2[j];
//        var exists = true
//
//        if (objects_equal(possible_match, current_location)) {
//            return true
//        }
//    }
//
//    return false;
//}
//
//function objects_equal(m1, m2) {
//    for (var key in m1) {
//        if (m1[key] !== m2[key])
//            return false;
//    }
//
//    return true;
//}
//
//function surgeon_exists(surgeon, current_search) {
//    var i;
//    var locations_1 = JSON.parse(surgeon.locations)
//
//    for (i = 0; i < current_search.length; i++) {
//        var current_surgeon = current_search[i];
//        var equal = locations_equal(current_surgeon, surgeon);
//
//        if (equal) return equal;
//    }
//
//    return false;
//}
//
//function get_location_title(location_json) {
//    var locations = JSON.parse(location_json);
//    if (locations.length > 0)
//        return locations[0].location_title;
//    return '';
//}
//
//function create_surgeon_info_html(surgeon) {
//    var html_args = [
//        `<div class='title'>${surgeon['title']}</div>`
//    ];
//
//    var locations = JSON.parse(surgeon["locations"]);
//
//    locations.forEach(location => {
//        location_title = location["location_title"];
//        html_args.push(`<div class='location-title'>${location_title}</div>`);
//
//        address = location["address"];
//        address_args = address.split("|");
//
//        address_args.forEach(address_arg => {
//            html_args.push(`<div class='address-text'>${address_arg}</div>`)
//        })
//    });
//
//    if (surgeon.phone) {
//        html_args.push(
//            `<div class='detail-label'>Phone</div>`
//        )
//        html_args.push(
//            `<div class='phone-text'>${surgeon.phone}</div>`
//        );
//    }
//
//    if (surgeon.training) {
//        html_args.push(
//            `<div class='detail-label'>Training</div>`
//        )
//        training = JSON.parse(surgeon.training);
//        training.forEach(training_text => {
//            training_text_args = training_text.split("|")
//            training_text_args.forEach(arg => {
//                html_args.push(
//                    `<div class='training-text'>${arg}</div>`
//                )
//            })
//            html_args.push(
//                `<hr/>`
//            )
//        })
//    }
//
//    return html_args.join("")
//
//}
//
//function reset(arg) {
//
//    info_windows.forEach(iw => {
//        iw.close();
//    })
//
//    reset_marker_cluster(all_markers)
//    // markerClusterer.setMaxZoom(mapOptions.zoom);
//
//    map.setCenter(mapOptions.center);
//    map.setZoom(mapOptions.zoom);
//
//    if ($(".results-container").find(".fas").hasClass("fa-caret-up"))
//        show_hide_results(null);
//
//}
//
//var latlngs_already = [];
//
//function create_marker(surgeon, map) {
//
//}
//
//function create_markers(surgeon, map) {
//    var latlngs = surgeon["latlng"].split("|")
//
//    var current_markers = [];
//
//    latlngs.forEach(latlng => {
//        if (latlngs_already.indexOf(latlng) === -1) {
//            latlngs_already.push(latlng);
//
//            var latlng_split = latlng.split(",");
//
//            var lat_lng = {
//                lat: parseFloat(latlng_split[0]),
//                lng: parseFloat(latlng_split[1])
//            }
//
//            var marker = new google.maps.Marker({
//                position: lat_lng,
//                map: map,
//                title: `${surgeon.title}||${surgeon.latlng}`
//            });
//
//            var surgeon_info_html = create_surgeon_info_html(surgeon);
//
//            marker.addListener('click', function () {
//                var infowindow = new google.maps.InfoWindow({
//                    content: surgeon_info_html
//                });
//                info_windows.push(infowindow)
//                infowindow.open(map, marker)
//            });
//
//            current_markers.push(marker);
//        }
//    })
//
//    return current_markers;
//}
//
//function reset_marker_cluster(markers) {
//    if (markerClusterer) {
//        markerClusterer.clearMarkers();
//        markerClusterer.addMarkers(markers);
//        // markerClusterer.repaint()
//    } else {
//
//        markerClusterer = new MarkerClusterer(map, markers,
//            { imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m' });
//    }
//}
//
//function center_map(lat, lng) {
//    map.setCenter({
//        lat: lat,
//        lng: lng,
//    })
//    map.setZoom(11)
//}
//
//function center_users_location() {
//    if (navigator.geolocation) {
//        navigator.geolocation.getCurrentPosition(center_map);
//    } else {
//        console.log("Geo Location not supported");
//    }
//}
//
//
