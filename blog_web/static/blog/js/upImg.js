/**
 * Created by lizhenya on 2018/5/19.
 */

function upload_start(){

    file_photo_view();
}

function file_photo_view(){
    jQuery(".file_photo").change(function(){
        var that = this;
        jQuery(".preview").each(function(i){
            if(i == 0){
                width = 0;
                height = 0;
            }else if(i == 1){
                width = 120;
                height = 120;
            }else{
                width = 48;
                height = 48;
            }
            previewImage(that,i,width,height);
        });
        jQuery(".update_show_button").show();
    });
}
function previewImage(file,i,width,height)
{
    var MAXWIDTH  = width;
    var MAXHEIGHT = height;
    var div = document.getElementById('preview_'+i);
    if (file.files && file.files[0])
    {
        div.innerHTML = '<img id=imghead_'+i+'>';
        var img = document.getElementById('imghead_'+i);
        img.onload = function(){
            var rect = clacImgZoomParam(MAXWIDTH, MAXHEIGHT, img.offsetWidth, img.offsetHeight);
            img.width = rect.width;
            img.height = rect.height;
            img.style.marginLeft = rect.left+'px';
            img.style.marginTop = rect.top+'px';
        }
        var reader = new FileReader();
        reader.onload = function(evt){img.src = evt.target.result;}
        reader.readAsDataURL(file.files[0]);
    }
    else
    {
        var sFilter='filter:progid:DXImageTransform.Microsoft.AlphaImageLoader(sizingMethod=scale,src="';
        file.select();
        var src = document.selection.createRange().text;
        div.innerHTML = '<img id=imghead_'+i+'>';
        var img = document.getElementById('imghead_'+i);
        img.filters.item('DXImageTransform.Microsoft.AlphaImageLoader').src = src;
        var rect = clacImgZoomParam(MAXWIDTH, MAXHEIGHT, img.offsetWidth, img.offsetHeight);
        status =('rect:'+rect.top+','+rect.left+','+rect.width+','+rect.height);
        div.innerHTML = "<div id=divhead_"+i+" style='width:"+rect.width+"px;height:"+rect.height+"px;margin-top:"+rect.top+"px;margin-left:"+rect.left+"px;"+sFilter+src+"\"'></div>";
    }
}
function clacImgZoomParam( maxWidth, maxHeight, width, height ){
    var param = {top:0, left:0, width:width, height:height};
    if( width>maxWidth || height>maxHeight )
    {
        rateWidth = width / maxWidth;
        rateHeight = height / maxHeight;

        if( rateWidth > rateHeight )
        {
            param.width =  maxWidth;
            param.height = Math.round(height / rateWidth);
        }else
        {
            param.width = Math.round(width / rateHeight);
            param.height = maxHeight;
        }
    }

    param.left = Math.round((maxWidth - param.width) / 2);
    param.top = Math.round((maxHeight - param.height) / 2);
    return param;
}
