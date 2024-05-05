// source: https://www.youtube.com/watch?v=PGtv-dBi2wE&ab_channel=TheArtofCode

#define MAX_STEPS 100
#define MAX_DIST 100.0
#define MIN_SURF_DIST 0.01

/*A sphere's signed distance field. Can be used to render spheres in 3d*/
float sphereSDF(vec3 targetPoint, vec3 sphereCenter, float radius) {
    return length(targetPoint - sphereCenter) - radius;
}

/*A 2d plane's signed distance field in 3d*/
float planeSDF(vec3 targetPoint, vec3 pointOnPlane, vec3 planeNormalVector) {
    return dot(targetPoint - pointOnPlane, planeNormalVector);
}

float GetDistanceFromSurface(vec3 point) {
    float sphereDist = sphereSDF(point, vec3(0.0, 1.0, 6.0), 1.0);
    float planeDist = planeSDF(point, vec3(0.0), vec3(0.0, 1.0, 0.0));

    float minDistanceFromObjects = min(sphereDist, planeDist);
    return minDistanceFromObjects;
}

float RayMarch(vec3 rayOrigin, vec3 rayDirection) {
    float distanceMarchedFromOrigin = 0.0;

    // ray marching loop
    for (int marchStep=0; marchStep < MAX_STEPS; marchStep++) {
        vec3 currentLocation = rayOrigin + rayDirection * distanceMarchedFromOrigin;
        // get a conservative estimate (a.k.a lower bound) of the distance to the scene
        float distanceLBFromScene = GetDistanceFromSurface(currentLocation); // all shapes in the scene are inside this funciton
        distanceMarchedFromOrigin += distanceLBFromScene;
        if ((distanceMarchedFromOrigin > MAX_DIST)  // marched too far
            || (distanceLBFromScene < MIN_SURF_DIST)) // we are already very close to the surface so no need to march further
            break;
    }

    return distanceMarchedFromOrigin;
}

vec3 GetNormal(vec3 point) {
    float distanceFromSurface = GetDistanceFromSurface(point);
    vec2 epsilon = vec2(0.01, 0.0);

    vec3 normal = vec3(
        GetDistanceFromSurface(point + epsilon.xyy),
        GetDistanceFromSurface(point + epsilon.yxy),
        GetDistanceFromSurface(point + epsilon.yyx)
    ) - distanceFromSurface;

    return normalize(normal);
}

float GetLight(vec3 pointOnSurface) {
    vec3 lightPosition = vec3(0, 5, 6); // right above the sphere
    // vec3 lightPosition = vec3(4, 1, 6); // to the left of the sphere

    lightPosition.xz += vec2(sin(iTime), cos(iTime)) * 2.0;

    vec3 lightVector = normalize(lightPosition - pointOnSurface);

    vec3 surfaceNormal = GetNormal(pointOnSurface);

    float diffusedLighting = clamp(dot(surfaceNormal, lightVector), 0.0, 1.0);

    // add shawdows by ray marching from the surface to the light and see if
    // the distance is less than shortest path between the light and the point
    // if it is then it means we hit something in between and the point should be in the shadow
    // move away from the surface a little before starting the ray march or else
    // the second ray march loop will exit right away as the loop break condition is already met
    float rayMarchDistanceFromPointToLight = RayMarch(pointOnSurface + surfaceNormal * MIN_SURF_DIST * 2.0, lightVector);

    if (rayMarchDistanceFromPointToLight < length(lightPosition - pointOnSurface)) {
        diffusedLighting *= 0.1;
    }

    return diffusedLighting;
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
    
    // start from black canvas
    vec3 pixelColor = vec3(0);
    
    // camera is at x=0, y=1, z=0
    vec3 cameraPosition = vec3(0., 1., 0.);

    // imagine if camera was at origin and the shader screen was 
    // parallel to xy plane and centered at x=0, y=0, z=1
    // then the vector from camera (origin) to the pixel would be
    // the direction of the ray corresponding to that pixel
    // x is negative to account for x-axis being to the left isntead of right
    vec3 rayDirection = normalize(vec3(-1.0 * originalPixelLocation.x, originalPixelLocation.y, 1.0));

    float distanceToSurface = RayMarch(cameraPosition, rayDirection);

    vec3 pointOnSurface = cameraPosition + rayDirection * distanceToSurface;

    float diffusedLighting = GetLight(pointOnSurface);

    pixelColor = vec3(diffusedLighting);

    outputPixelColor = vec4(pixelColor,1.0);
}