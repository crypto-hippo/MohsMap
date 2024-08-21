async function setup_map() {
    const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary("marker");
    const { Map, InfoWindow } = await google.maps.importLibrary("maps");
    const base_url = "http://localhost:5000" || "https://mohsmap.uc.r.appspot.com"
    let map;
    let marker_clusterer;
    let markers = []
    let surgeons = []
    let map_options = get_map_options()

    const infoWindow = new google.maps.InfoWindow({
        content: "",
        disableAutoPan: true,
    });
    
    function get_map_options() {
        return {
            center: {
                lat: 38.755,
                lng: -98.82
            },
            zoom: 4,
            mapId: "bruh"
        };
    }

    function open_info_window(surgeon, marker) {
        let info_window_content = create_popup_content(surgeon);
        infoWindow.setContent(info_window_content);
        infoWindow.open(map, marker);
    }

    async function get_surgeons() {
        let resp = await fetch(`${base_url}/surgeon/get`);
        let surgeons = await resp.json();
        return surgeons;
    }

    function create_popup_content(s) {
        divs = "";
        divs += `<div class="popup-title">${s.name_text}</div>`
        s.location_divs.forEach(d => {
            let new_div = `<div class="popup-data">${d}</div>`;
            divs += new_div;
        });
        return divs;
    }

    function init_surgeon_markers() {
        surgeons.forEach(s => {
            let next_marker = new AdvancedMarkerElement({
                map: map,
                position: {lat: parseFloat(s.lat), lng: parseFloat(s.lng)},
                title: s.name_text,
            });
            next_marker.addListener("click", () => {
                open_info_window(s, next_marker);
            });
          
            markers.push(next_marker);
        })
        marker_clusterer = new markerClusterer.MarkerClusterer({ markers, map });
    }

    window.reset_map = function() {
        $('.results-container').empty();
        markers.forEach(m => {
            m.setMap(null);
        });
        markers = []
        map = new Map(document.getElementById("map"), map_options);
        init_surgeon_markers();
    }


    window.search = async function() {
        let search_input = $("#search").val().trim();
        if (search_input.length > 0) {
            let search_results = await fetch(`${base_url}/surgeon/search`, {
                "method": "post",
                "headers": {"content-type": "application/json"},
                "body": JSON.stringify({"search_value": search_input})
            })

            let json_data = await search_results.json();

            $('.results-container').empty();

            json_data.forEach(s => {
                let result = `<div class="result" data-lat="${s.lat}" data-lng="${s.lng}">${s.name_text}</div>`
                $('.results-container').append(result);
            });

            $('.result').click(function(e) {
                let lat = parseFloat(e.target.getAttribute("data-lat"));
                let lng = parseFloat(e.target.getAttribute("data-lng"));
                markers.forEach(m => {
                    let m_lat = m.position.Fg;
                    let m_lng = m.position.Gg;
                    if (m_lat === lat && m_lng === lng) {
                        let surgeon = surgeons.filter(s => {
                            let s_lat = parseFloat(s.lat);
                            let s_lng = parseFloat(s.lng);
                            return s.name_text === e.target.innerText && s_lat === m_lat && s_lng === m_lng;
                        })[0];
                        map.setZoom(17)
                        map.panTo(m.position);
                        open_info_window(surgeon, m);
                    }
                });
            })
        }
    }   

    window.onkeyup = function() {
        let search_input = $("#search").val().trim();
        if (search_input.length > 0) {
            window.search();
        }
    }

    async function initMap() {
        map = new Map(document.getElementById("map"), map_options);
        surgeons = await get_surgeons();
        init_surgeon_markers();
    }

    initMap();
}

setup_map();