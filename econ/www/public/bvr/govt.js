var Log = {
    elem: false,
    write: function(text){
        if (!this.elem) 
            this.elem = document.getElementById('log');
        this.elem.innerHTML = text;
        this.elem.style.left = (500 - this.elem.offsetWidth / 2) + 'px';
    }
};

function addEvent(obj, type, fn) {
    if (obj.addEventListener) obj.addEventListener(type, fn, false);
    else obj.attachEvent('on' + type, fn);
};


function init(json){
    var infovis = document.getElementById('infovis');
    var w = infovis.offsetWidth, h = infovis.offsetHeight;
    infovis.style.width = w + 'px';
    infovis.style.height = h + 'px';
    
    //init tm
    var tm = new TM.Squarified({
        //Where to inject the treemap.
        rootId: 'infovis',
        titleHeight: 17,  

        //Add click handlers for
        //zooming the Treemap in and out
        addLeftClickHandler: true,
        addRightClickHandler: true,
        
        //When hovering a node highlight the nodes
        //between the root node and the hovered node. This
        //is done by adding the 'in-path' CSS class to each node.
        selectPathOnHover: true,
                
        Color: {
            //Allow coloring
            allow: true,
            //Set min value and max value constraints
            //for the *$color* property value.
            //Default's to -100 and 100.
            minValue: 1,
            maxValue: 50,
            //Set color range. Default's to reddish and greenish.
            //It takes an array of three
            //integers as R, G and B values.
            minColorValue: [0, 255, 50],
            maxColorValue: [255, 0, 50]
        },
        
        //Allow tips
        Tips: {
          allow: true,
          //add positioning offsets
          offsetX: 20,
          offsetY: 20,
          //implement the onShow method to
          //add content to the tooltip when a node
          //is hovered
          onShow: function(tip, node, isLeaf, domElement) {
              tip.innerHTML = "<div class=\"tip-title\">" + node.name + "</div>" + 
                "<div class=\"tip-text\">" + this.makeHTMLFromData(node.data) + "</div>"; 
          },  

          //Build the tooltip inner html by taking each node data property
          makeHTMLFromData: function(data){
              var html = '';
              html += "Spending (£m)" + ': ' + data.$area + '<br />';
              if ("$color" in data) 
                  html += "rank" + ': ' + data.$color + '<br />';
              if ("image" in data) 
                  html += "<img class=\"album\" src=\"" + data.image + "\" />";
              return html;
          }
        },

        //Remove all element events before destroying it.
        onDestroyElement: function(content, tree, isLeaf, leaf){
            if(leaf.clearAttributes) leaf.clearAttributes();
        }
    });
    
    //load JSON and plot
    tm.loadJSON(json);
    //end

    document.getElementById('out_button').onclick = function(){
        tm.out();
    };
}
