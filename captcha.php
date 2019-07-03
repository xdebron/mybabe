<?php
set_time_limit(0);

//variables used by mybb captcha.php
$img_width = 200;
$img_height = 60;

$min_size = 20;
$max_size = 32;

$min_angle = -30;
$max_angle = 30;




//actually this code belongs to mybb captcha.php too i dont need to change it.

$ttf_fonts = array();
$ttfdir  = @opendir("fonts");
if($ttfdir !== false)
{
    while(($file = readdir($ttfdir)) !== false)
    {
        // If this file is a ttf file, add it to the list
        if(is_file("fonts/".$file))
        {
            $ttf_fonts[] = "fonts/".$file;
        }
    }
    closedir($ttfdir);
}


for($j=0;$j<300000;$j++)
{
    //seed random everytime
    mt_srand(300001+$j);
    
    //create dataset 10-1 ratio
    for($i=0;$i<10;$i++)
    {
        create_captcha("train");
    }
    create_captcha("test");
}

//Anything below this line are belong to mybb captcha.php
function create_captcha($folder)
{
    $im = imagecreatetruecolor($img_width, $img_height);


        // Fill the background with white
        $bg_color = imagecolorallocate($im, 255, 255, 255);
        imagefill($im, 0, 0, $bg_color);

        // Draw random circles, squares or lines?
        $to_draw = mt_rand(0, 2);
        if($to_draw == 1)
        {
            draw_circles($im);
        }
        else if($to_draw == 2)
        {
            draw_squares($im);
        }
        else
        {
            draw_lines($im);
        }

        // Draw dots on the image
        draw_dots($im);

        // Write the image string to the image
        $filename = draw_string($im, generateRandomString(5));
        //echo $filename;

        // Draw a nice border around the image
        $border_color = imagecolorallocate($im, 0, 0, 0);
        imagerectangle($im, 0, 0, $img_width-1, $img_height-1, $border_color);

        // Output the image
        //header("Content-type: image/png");
        ob_start();
        imagepng($im);
        $imagedata = ob_get_contents();
        ob_end_clean();
        file_put_contents("dataset/".$folder."/".$filename."_".md5($imagedata).".png", $imagedata);
        imagedestroy($im);
}
function draw_lines(&$im)
{
	global $img_width, $img_height;

	for($i = 10; $i < $img_width; $i += 10)
	{
		$color = imagecolorallocate($im, mt_rand(150, 255), mt_rand(150, 255), mt_rand(150, 255));
		imageline($im, $i, 0, $i, $img_height, $color);
	}
	for($i = 10; $i < $img_height; $i += 10)
	{
		$color = imagecolorallocate($im, mt_rand(150, 255), mt_rand(150, 255), mt_rand(150, 255));
		imageline($im, 0, $i, $img_width, $i, $color);
	}
}

/**
 * Draws a random number of circles on the image.
 *
 * @param resource $im The image.
 */
function draw_circles(&$im)
{
	global $img_width, $img_height;

	$circles = $img_width*$img_height / 100;
	for($i = 0; $i <= $circles; ++$i)
	{
		$color = imagecolorallocate($im, mt_rand(180, 255), mt_rand(180, 255), mt_rand(180, 255));
		$pos_x = mt_rand(1, $img_width);
		$pos_y = mt_rand(1, $img_height);
		$circ_width = ceil(mt_rand(1, $img_width)/2);
		$circ_height = mt_rand(1, $img_height);
		imagearc($im, $pos_x, $pos_y, $circ_width, $circ_height, 0, mt_rand(200, 360), $color);
	}
}

/**
 * Draws a random number of dots on the image.
 *
 * @param resource $im The image.
 */
function draw_dots(&$im)
{
	global $img_width, $img_height;

	$dot_count = $img_width*$img_height/5;
	for($i = 0; $i <= $dot_count; ++$i)
	{
		$color = imagecolorallocate($im, mt_rand(200, 255), mt_rand(200, 255), mt_rand(200, 255));
		imagesetpixel($im, mt_rand(0, $img_width), mt_rand(0, $img_height), $color);
	}
}

/**
 * Draws a random number of squares on the image.
 *
 * @param resource $im The image.
 */
function draw_squares(&$im)
{
	global $img_width, $img_height;

	$square_count = 30;
	for($i = 0; $i <= $square_count; ++$i)
	{
		$color = imagecolorallocate($im, mt_rand(150, 255), mt_rand(150, 255), mt_rand(150, 255));
		$pos_x = mt_rand(1, $img_width);
		$pos_y = mt_rand(1, $img_height);
		$sq_width = $sq_height = mt_rand(10, 20);
		$pos_x2 = $pos_x + $sq_height;
		$pos_y2 = $pos_y + $sq_width;
		imagefilledrectangle($im, $pos_x, $pos_y, $pos_x2, $pos_y2, $color);
	}
}

/**
 * Writes text to the image.
 *
 * @param resource $im The image.
 * @param string $string The string to be written
 *
 * @return bool False if string is empty, true otherwise
 */
function draw_string(&$im, $string)
{
	global $use_ttf, $min_size, $max_size, $min_angle, $max_angle, $ttf_fonts, $img_height, $img_width;
    $filename=$string."_";
	if(empty($string))
	{
		return false;
	}

	$spacing = $img_width / strlen($string);
	$string_length = strlen($string);
	for($i = 0; $i < $string_length; ++$i)
	{
		// Using TTF fonts
        // Select a random font size
        $font_size = rand($min_size, $max_size);

        // Select a random font
        $font = array_rand($ttf_fonts);
        $font = $ttf_fonts[$font];

        // Select a random rotation
        $rotation = rand($min_angle, $max_angle);

        // Set the colour
        $r = mt_rand(0, 200);
        $g = mt_rand(0, 200);
        $b = mt_rand(0, 200);
        $color = imagecolorallocate($im, $r, $g, $b);


        // Fetch the dimensions of the character being added
        $dimensions = imageftbbox($font_size, $rotation, $font, $string[$i], array());
        $string_width = $dimensions[2] - $dimensions[0];
        $string_height = $dimensions[3] - $dimensions[5];

        // Calculate character offsets
        $pos_x = $spacing / 4 + $i * $spacing;
        $pos_y = ceil(($img_height-$string_height/2));
        
        
        // Draw a shadow
        $shadow_x = rand(-3, 3) + $pos_x;
        $shadow_y = rand(-3, 3) + $pos_y;
        $shadow_color = imagecolorallocate($im, $r+20, $g+20, $b+20);
        imagefttext($im, $font_size, $rotation, $shadow_x, $shadow_y, $shadow_color, $font, $string[$i], array());

        // Write the character to the image
        $locations=imagefttext($im, $font_size, $rotation, $pos_x, $pos_y, $color, $font, $string[$i], array());
        
        $black = imagecolorallocate($im, 0, 0, 0);
	}
	return $filename;
}

function generateRandomString($length = 10) {
    $characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    $charactersLength = strlen($characters);
    $randomString = '';
    for ($i = 0; $i < $length; $i++) {
        $randomString .= $characters[mt_rand(0, $charactersLength - 1)];
    }
    return $randomString;
}
