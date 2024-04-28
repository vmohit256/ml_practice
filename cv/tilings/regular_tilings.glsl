// rotation matrix for an angle
mat2 rotate2d(float _angle){
    return mat2(cos(_angle),-sin(_angle),
                sin(_angle), cos(_angle));
}

vec3 squareTiling(vec2 pixelLocation, vec3 tileColor1, vec3 tileColor2) {
    vec3 pixelColor = vec3(0);
    
    // assign color based on integer component of the locations
    // alternate colors in both x and y directions
    pixelColor += tileColor1 * 0.5 * mod((floor(pixelLocation.x) + floor(pixelLocation.y)), 2.0);  
    pixelColor += tileColor2 * 0.5 * mod((floor(pixelLocation.x) + floor(pixelLocation.y) + 1.0), 2.0); 
    
    return pixelColor;
}

/*Method for generating equilateral triangle tiling:
Create a grid where heights of rows in y-coordinate is set to the height of a triangle
Draw an equilateral in each cell of odd rows and inverted eq. triangle in each cell of even row
*/
vec3 equilateralTriangleTiling(vec2 pixelLocation, vec3 tileColor1, vec3 tileColor2) {
    vec3 pixelColor = vec3(0);

    // squish y-coordinate spacings of the grid
    pixelLocation.y *= (2.0 / 1.732); 
    
    // flip alternate rows upside down so we just need to draw upright triangles and 
    // inverted triangles are generated atomatically by reflection
    pixelLocation.y = pixelLocation.y * mod(floor(pixelLocation.y), 2.0) + (1.0 - pixelLocation.y) * mod(floor(pixelLocation.y) + 1.0, 2.0);
    
    // swap the two colors between each row
    vec3 selectedTileColor1 = tileColor1 * mod(floor(pixelLocation.y), 2.0) + tileColor2 * mod(floor(pixelLocation.y) + 1.0, 2.0);
    vec3 selectedTileColor2 = tileColor2 * mod(floor(pixelLocation.y), 2.0) + tileColor1 * mod(floor(pixelLocation.y) + 1.0, 2.0);
    
    // operate on fractional part to replicate it in each grid cell
    pixelLocation = fract(pixelLocation);
    // reflect it along y-axis so that we only need to draw half of the triangle
    pixelLocation = abs(pixelLocation-vec2(0.5, 0));
    
    // split the half cell region into one where 2x+y-1 is > 0 or < 0
    // assign colors appropriately to each region to obtain the tiling
    pixelColor += selectedTileColor1 * 0.5 * step(0.0, 1.0 - 2.0 * pixelLocation.x - pixelLocation.y);  
    pixelColor += selectedTileColor2 * 0.5 * (1.0 - step(0.0, 1.0 - 2.0 * pixelLocation.x - pixelLocation.y)); 
    
    return pixelColor;
}

/*Method for generating regular hexagon tiling:
Stretch x-spacing to sqrt(3). Alternate these 3 types of rows:
type-1: draw alternate rectangles
type-2 and 3: draw flipped quarter part of hexagons facing away from each other
operate on absolute value of (x, y) - 0.5 to take advantage of symmetry
*/
vec3 regularHexagonalTiling(vec2 pixelLocation, vec3 tileColor1, vec3 tileColor2, vec3 tileColor3) {
    vec3 pixelColor = vec3(0);

    // move a little to center to the center of a hexagon
    pixelLocation.y -= 1.0;

    // expand x-spacing by sqrt(3)
    pixelLocation.x /= 1.732;

    // fill in first row type with alternate rectangles
    float isFirstRow = float(mod(floor(pixelLocation.y), 3.0) == 0.0);
    float isSecondRow = float(mod(floor(pixelLocation.y), 3.0) == 1.0);
    float isThirdRow = float(mod(floor(pixelLocation.y), 3.0) == 2.0);

    vec3 shuffledColor1 = float(mod(floor(pixelLocation.x), 3.0) == 0.0) * tileColor1
        + float(mod(floor(pixelLocation.x), 3.0) == 1.0) * tileColor2
        + float(mod(floor(pixelLocation.x), 3.0) == 2.0) * tileColor3;

    vec3 shuffledColor2 = float(mod(floor(pixelLocation.x), 3.0) == 0.0) * tileColor2
        + float(mod(floor(pixelLocation.x), 3.0) == 1.0) * tileColor3
        + float(mod(floor(pixelLocation.x), 3.0) == 2.0) * tileColor1;

    vec3 shuffledColor3 = float(mod(floor(pixelLocation.x), 3.0) == 0.0) * tileColor3
        + float(mod(floor(pixelLocation.x), 3.0) == 1.0) * tileColor1
        + float(mod(floor(pixelLocation.x), 3.0) == 2.0) * tileColor2;

    pixelColor += isFirstRow * shuffledColor1;

    // move to cell level locations
    pixelLocation = fract(pixelLocation);

    // flip the second row as it is just a reflection of the 3rd row
    pixelLocation.y = pixelLocation.y * (isFirstRow + isThirdRow) + (1.0 - pixelLocation.y) * isSecondRow;

    // flip around x=0.5 line
    float isFlippedAlongXequalsHalf = float(pixelLocation.x < 0.5);

    pixelLocation = abs(pixelLocation-vec2(0.5, 0));

    float isRegion1 = (1.0 - isFirstRow) * float((pixelLocation.y - pixelLocation.x - 0.5) >= 0.0);
    float isRegion2 = (1.0 - isFirstRow) * (1.0 - isRegion1);

    // region 1 is always the same color as the rectangle in first row
    pixelColor += isRegion1 * shuffledColor1;
    
    // region2 is 3rd color if it was not flipped along x=0.5. Otherwise it is 2nd color
    pixelColor += isRegion2 * (isFlippedAlongXequalsHalf * shuffledColor2 + (1.0 - isFlippedAlongXequalsHalf) * shuffledColor3);

    return pixelColor;
}

/*
This function is called for each value of pixelCoordinate on the screen to compute its color

bottom left is (0, 0) and top right is (800, 450), assuming the screensize is 800 x 450

outputPixelColor has 4 dimensions: Red, Green, Blue, Alpha. 
Alpha is transparency level where 0.0 means fully transparent (invisible) and 1.0 means fully opaque (solid).
RGB vary from 0 to 1, so (0, 0, 0) is black and (1, 1, 1) is white
*/
void mainImage(out vec4 outputPixelColor, in vec2 pixelCoordinate)
{
    // center on origin and make y vary from -0.5 to 0.5
    // iResolution is (800, 450) if that is the resolution
    vec2 originalPixelLocation = (pixelCoordinate - 0.5 * iResolution.xy) / iResolution.y;
    
    // iMouse is the location of mouse
    vec2 mouseLocation = (iMouse.xy - 0.5 * iResolution.xy) / iResolution.y;
    
    // these colors are used to color the tiles
    vec3 tileColor1 = vec3(1.0, 0.0, 0.0); // 0.66 * vec3(1.0, 1.0, 1.0);
    vec3 tileColor2 = vec3(0.0, 1.0, 0.0); // 0.33 * vec3(1.0, 1.0, 1.0);
    vec3 tileColor3 = vec3(0.0, 0.0, 1.0); // 0.0 * vec3(1.0, 1.0, 1.0);
    
    // if enabled, then the second layer of tiling is rotated while the first layer is fixed
    // WARNING: rotation animation can be disorienting
    bool rotationEnabled = false; 
    // if rotation is enabled, then the animation pauses this many seconds on the fully aligned state
    float pauseDuration = 0.3;
    float pi = 3.1415;
    
    // zoom in or zoom out by scaling the location
    vec2 pixelLocation = originalPixelLocation * 12.0;

    // start from black canvas
    vec3 pixelColor = vec3(0);
    
    // add the color of the first tiling
    //pixelColor += squareTiling(pixelLocation, tileColor1, tileColor2);
    pixelColor += equilateralTriangleTiling(pixelLocation, tileColor1, tileColor2);
    //pixelColor += regularHexagonalTiling(pixelLocation, tileColor1, tileColor2, tileColor3);

    float secondTileLayerAngle = 2.0 * pi;
    if (rotationEnabled) {
        // tune the speed of rotation by changing the constant multiplied with iTime
        // iTime is the seconds passed since creation
        secondTileLayerAngle = iTime / 5.0;
        secondTileLayerAngle = secondTileLayerAngle - (min(pauseDuration, mod(secondTileLayerAngle, 2.0 * pi)));
    }
    
    // rotate the location before adding the second tiling layer
    pixelLocation = rotate2d(secondTileLayerAngle) * pixelLocation;
    
    // add the color of the second tiling
    //pixelColor += squareTiling(pixelLocation, tileColor1, tileColor2);
    pixelColor += equilateralTriangleTiling(pixelLocation, tileColor1, tileColor2);
    //pixelColor += regularHexagonalTiling(pixelLocation, tileColor1, tileColor2, tileColor3);
    
    // display a cross at the center
    pixelColor = pixelColor * step(0.003, min(abs(originalPixelLocation.x), abs(originalPixelLocation.y)));
    pixelColor.r += 1.0 - step(0.003, min(abs(originalPixelLocation.x), abs(originalPixelLocation.y)));

    outputPixelColor = vec4(pixelColor,1.0);
}