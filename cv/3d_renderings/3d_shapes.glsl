// a repository of shapes to use in projects

// sources: https://www.youtube.com/watch?v=Ff0jJyyiVyw&list=PLGmrMu-IwbgtMxMiV3x4IrHPlPmg7FD-P&ab_channel=TheArtofCode
// https://www.shadertoy.com/view/WtGXDD

#define MAX_STEPS 100
#define MAX_DIST 100.0
#define MIN_SURF_DIST 0.01
#define PI 3.141592

mat2 RotationMatrix(float angle) {
    return mat2(cos(angle), -sin(angle), sin(angle), cos(angle));
}

/*A sphere's signed distance field. Can be used to render spheres in 3d*/
float sphereSDF(vec3 targetPoint, vec3 sphereCenter, float radius) {
    return length(targetPoint - sphereCenter) - radius;
}

/*A 2d plane's signed distance field in 3d*/
float planeSDF(vec3 targetPoint, vec3 pointOnPlane, vec3 planeNormalVector) {
    return dot(targetPoint - pointOnPlane, planeNormalVector);
}

/*Plane SDF given three points on the plane. Order of the points decides
the orientation. Normal is given by cross product of (p2 - p1) x (p3 - p2)
*/
float planeSDF(vec3 targetPoint, vec3 point1, vec3 point2, vec3 point3) {
    vec3 normalVector = normalize(cross(point2-point1, point3-point2));
    return planeSDF(targetPoint, point1, normalVector);
}

float capsuleSDF(vec3 targetPoint, vec3 pointA, vec3 pointB, float radius) {
    vec3 vectorAtoB = pointB - pointA;
    vec3 vectorAtoTarget = targetPoint - pointA;

    // t is the linear interpolation co-efficient between a and b
    // it represents the closest point to the target point on the line segment
    // the closest point is given as t*b + (1-t)*a
    float t = dot(vectorAtoTarget, vectorAtoB) / dot(vectorAtoB, vectorAtoB);
    t = clamp(t, 0.0, 1.0);
    vec3 closestPointToTargetOnLineSegment = t * pointB + (1.0 - t) * pointA;
    return length(targetPoint - closestPointToTargetOnLineSegment) - radius;
}

float torusSDF(vec3 targetPoint, vec3 torusCenter, vec3 torusPlaneNormal, float torusRadius, float torusThickness) {
    // idea: distance from torus = distance of target point from the closest point on the ring - radius
    // project the parget point onto the plane of the torus. Call projected point p
    // closest point on the ring is radius * unit vector from center to p

    vec3 centerToTargetPoint = targetPoint - torusCenter;
    vec3 centerToProjectedPoint = centerToTargetPoint - dot(centerToTargetPoint, torusPlaneNormal) * torusPlaneNormal;
    vec3 closestPointOnRingToTheTarget = torusCenter + torusRadius * normalize(centerToProjectedPoint);
    return length(targetPoint - closestPointOnRingToTheTarget) -  torusThickness;
}

float boxSDF(vec3 targetPoint, vec3 boxCenter, vec3 boxDimensions) {
    vec3 positionRelativeToBoxCenter = targetPoint - boxCenter;
    vec3 weirdVectorThatICantGiveAGoodName = abs(positionRelativeToBoxCenter) - boxDimensions / 2.0;

    // 2nd term is for when the point is inside the box so we should return negative distance
    // if we don't do this, we get spooky (but cool!) artifacts on the box's surface
    return length(max(weirdVectorThatICantGiveAGoodName, 0.0))
        + min(max(max(weirdVectorThatICantGiveAGoodName.x, weirdVectorThatICantGiveAGoodName.y), 
            weirdVectorThatICantGiveAGoodName.z), 0.);
}

float regularOctahedronSDF(vec3 p) {
    return planeSDF(abs(p), vec3(1.0, 0.0, 0.0), normalize(vec3(1.0)));
}

float cubeSDF(vec3 p) {
    return boxSDF(p, vec3(0.0), vec3(1.0));
}

float regularTetrahedronSDF(vec3 p) {
    // the below code is copied from this shader: https://www.shadertoy.com/view/Ws23zt
    // strategy: take intersection of two v-shaped infinite trains
    // one V shaped train going along y=x line with the sharp edge at z=-1
    // other inverted V shaped train along x+y=0 line with the sharp edge at z = 1

    // v shape is formed by reflecting the plane x - y - z = 1 along y = x plane
    // the side where x > y is reflected along y = x plane to psate the same thing 
    // in the region where x < y
    float distanceFromFirstVshape = (abs(p.x-p.y) - p.z - 0.5) / sqrt(3.0);

    // the below inverted V shape is formed in a similar way
    float distanceFromSecondInvertedVshape = (abs(p.x+p.y) + p.z - 0.5) / sqrt(3.0);

    // take intersection of the two V shaped infinite toblerons
    return max(distanceFromFirstVshape, distanceFromSecondInvertedVshape);
}

float regularDodecahedronInscribedCubeOppositeFacesSDF(vec3 p) {
    // this function give SDF of 4 planes corresponding to two opposite faces of the inscribed cube of 
    // regular dodecahedron from this image: https://www.matematicasvisuales.com/images/geometry/space/dodecahedron/zome/DSC_8969.jpg

    // first reflect along both y and z directions
    vec3 pReflectedAlongYandZ = vec3(p.x, abs(p.y), abs(p.z));

    // now apply the SDF of the plane that is in positive y and z space
    // it passes through the vertex (1, 1, 1) of the cube
    // and makes angle (dodecahedron dihedral angle) / 2 with the xz plane
    float normalAngle = (PI / 2.0) - (PI * 116.56505 / 180.0) / 2.0;
    return planeSDF(pReflectedAlongYandZ, vec3(0.5, 0.5, 0.5), normalize(vec3(0.0, sin(normalAngle), cos(normalAngle))));
}

float regularDodecahedronSDF(vec3 p) {
    // this video explains why dihedral angle of dodecahedron is 116.56505 = 2 arcsin(cos(36) / cos(18))
    // https://www.youtube.com/watch?v=PepzbC9I_wI&ab_channel=FredB%27sTechChannel
    // wow! a cube can be inscribed into a regular dodecahedron! That makes it so much easier!
    // https://www.matematicasvisuales.com/english/html/geometry/space/dodecahedroncube.html
    // the below construction is based on this image below taken from the above link
    // https://www.matematicasvisuales.com/images/geometry/space/dodecahedron/zome/DSC_8969.jpg

    // strategy: break it into intersection of 3 sets of plane.
    // each set contains 4 planes each and they correspond to a face of the inscribed cube

    float distanceFromPlaneSet1 = regularDodecahedronInscribedCubeOppositeFacesSDF(p);

    // for plane set 2, remap xyz coordinates as follows:
    // x -> z, y -> -x, z -> -y
    vec3 remappedCoordinatesForPlaneSet2 = vec3(p.z, -p.x, -p.y);
    float distanceFromPlaneSet2 = regularDodecahedronInscribedCubeOppositeFacesSDF(remappedCoordinatesForPlaneSet2);

    // for plane set 3, remap xyz coordinates as follows:
    // x -> y, y -> -z, z -> -x
    vec3 remappedCoordinatesForPlaneSet3 = vec3(p.y, -p.z, -p.x);
    float distanceFromPlaneSet3 = regularDodecahedronInscribedCubeOppositeFacesSDF(remappedCoordinatesForPlaneSet3);

    // now intersect to form the regular dodecahedron! tada!
    return max(distanceFromPlaneSet1, max(distanceFromPlaneSet2, distanceFromPlaneSet3));
}

float pentagonalPyramidCapOfIcosahedronSDF(vec3 p) {
    // returns SDF for the pentagonal pyramid cap with the corner at (0, 1, 0)
    // reflect around yz plane to take advantage of some symmetry
    vec3 pReflectedOnYZplane = vec3(abs(p.x), p.y, p.z);

    // now draw the three planes in brute force fashion
    vec3 topVertex = vec3(0.0, 1.0, 0.0);
    
    float theta = atan(0.5, 1.0); // computed on paper

    // vertices on the base of the cap in counter-clockwise orientation. Starting from the vertex with 0 x-coordinate
    vec3 p1 = vec3(0.0, sin(theta), cos(theta));
    vec3 p2 = vec3(cos(theta) * sin(2.0 * PI / 5.0), sin(theta), cos(theta) * cos(2.0 * PI / 5.0));
    vec3 p3 = vec3(cos(theta) * sin(PI / 5.0), sin(theta), -cos(theta) * cos(PI / 5.0));
    vec3 p4 = vec3(-cos(theta) * sin(PI / 5.0), sin(theta), -cos(theta) * cos(PI / 5.0));

    // take intersection of the three plane sdfs on the reflected point
    return max(
            planeSDF(pReflectedOnYZplane, topVertex, p1, p2),
            max(
                planeSDF(pReflectedOnYZplane, topVertex, p2, p3),
                planeSDF(pReflectedOnYZplane, topVertex, p3, p4)
            )
        );
}

float regularIcosahedronSDF(vec3 p) {
    // TODO: use symmetry more and simplify the code
    // strategy: use brute force to calculate each point and construct planes while using some symmetry
    // assume the icosahedron is inscribed in unit circle.
    // points (0, 1, 0) and (0, -1, 0) are the extremes endpoints repsenting the corners of the two pentagonal pyramid caps
    // then there are two flipped bases of pentagonal pyramids at heights sin(theta) and sin(-theta)
    // theta is calculated on paper and it turns out to be = arctan(0.5)
    
    // reflect in yz plane to take advantage of symmetry
    vec3 pReflectedOnYZplane = vec3(abs(p.x), p.y, p.z);

    float distanceFromTopCap = pentagonalPyramidCapOfIcosahedronSDF(p);

    float theta = atan(0.5, 1.0); // computed on paper
    
    // just brute force reflect the cap around 3 planes (one for each side of the pentagon base of the cap)
    // vertices on the base of the cap in counter-clockwise orientation. Starting from the vertex with 0 x-coordinate
    vec3 p1 = vec3(0.0, sin(theta), cos(theta));
    vec3 p2 = vec3(cos(theta) * sin(2.0 * PI / 5.0), sin(theta), cos(theta) * cos(2.0 * PI / 5.0));
    vec3 p3 = vec3(cos(theta) * sin(PI / 5.0), sin(theta), -cos(theta) * cos(PI / 5.0));
    vec3 p4 = vec3(-cos(theta) * sin(PI / 5.0), sin(theta), -cos(theta) * cos(PI / 5.0));

    // reflect along the plane (p1, p2, origin). Map all points with negative distance onto their reflected image with negative distance
    vec3 normal1 = normalize(cross(p2-p1, vec3(0.0)-p2));
    vec3 pReflectedOnPlane1 = pReflectedOnYZplane - 2.0 * normal1 * min(0.0, dot(normal1, pReflectedOnYZplane));
    float distanceFromCap1 = pentagonalPyramidCapOfIcosahedronSDF(pReflectedOnPlane1);

    // do the same thing for cap2
    vec3 normal2 = normalize(cross(p3-p2, vec3(0.0)-p3));
    vec3 pReflectedOnPlane2 = pReflectedOnYZplane - 2.0 * normal2 * min(0.0, dot(normal2, pReflectedOnYZplane));
    float distanceFromCap2 = pentagonalPyramidCapOfIcosahedronSDF(pReflectedOnPlane2);

    // finally one more time for cap3!
    vec3 normal3 = normalize(cross(p4-p3, vec3(0.0)-p4));
    vec3 pReflectedOnPlane3 = pReflectedOnYZplane - 2.0 * normal3 * min(0.0, dot(normal3, pReflectedOnYZplane));
    float distanceFromCap3 = pentagonalPyramidCapOfIcosahedronSDF(pReflectedOnPlane3);

    // take intersection of all caps to obtain the final icosahedron distance!
    float icosahedronDistance = max(distanceFromTopCap, max(distanceFromCap1, max(distanceFromCap2, distanceFromCap3)));

    return icosahedronDistance;
}

vec3 setMaxToZero(vec3 v) {
    // sets the max element of the vector to 0 but only if its between 0 and 1.1
    float maxVal = clamp(max(max(v.x, v.y), v.z), 0.0, 1.1);
    return vec3(v.x == maxVal ? 0.0 : v.x, v.y == maxVal ? 0.0 : v.y, v.z == maxVal ? 0.0 : v.z);
}


float GetDistanceFromSurface(vec3 point) {
    // float shapeDist = sphereSDF(point, vec3(0.0), 1.0);
    // float shapeDist = capsuleSDF(point, vec3(0.0, -1.0, -1.0), vec3(1.0, 0.0, 1.0), 0.2);
    // float shapeDist = torusSDF(point, vec3(0.0), normalize(vec3(0.0, 0.0, 1.0)), 1.0, 0.2);
    //float shapeDist = boxSDF(point, vec3(0.0), vec3(1.0, 0.5, 1.5));

    float shapeDist = regularOctahedronSDF(point);
    //float shapeDist = cubeSDF(point);
    // float shapeDist = regularTetrahedronSDF(point);
    // float shapeDist = regularDodecahedronSDF(point);
    // float shapeDist = regularIcosahedronSDF(point);

    // visualize grid lines and points

    vec3 gridDiffVector = abs(point - clamp(round(point), -2.0, 2.0));
    float gridPointsDist = length(gridDiffVector) - 0.02;

    float gridLinesDist = length(setMaxToZero(gridDiffVector)) - 0.0005;

    float gridDist = min(gridPointsDist, gridLinesDist);

    //float planeDist = planeSDF(point, vec3(0.0, -2.0, 0.0), vec3(0.0, 1.0, 0.0));
    //float minDistanceFromObjects = min(shapeDist, planeDist);

    float minDistanceFromObjects = min(shapeDist, gridDist);

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

/* Given the centered and aspect resolution corrected pixel location, return the ray direction that passes through
that pixel location if the ray originated from rayOrigin and the camera was oriented such that
its center pointed to the centerLocation. zoomFactor is how far away from camera is the projection plane.
increasing zoomFactor zooms the image by moving the projective plane away from the raOrigin
*/
vec3 GetRayDirection(vec2 originalPixelLocation, vec3 rayOrigin, vec3 centerLocation, float zoomFactor) {
    vec3 zAxisDirection = normalize(centerLocation - rayOrigin);
    // vec3(0, 1, 0) is the default y-axis direction so if zAxisDirection happens to coincide
    // with the actual z-axis (i.e. vec(0, 0, 1)) then x-axis will coincide with the actual
    // x-axis vec(1, 0, 0)
    vec3 xAxisDirection = normalize(cross(vec3(0, 1, 0), zAxisDirection));
    vec3 yAxisDirection = cross(zAxisDirection, xAxisDirection);
    return normalize(originalPixelLocation.x * xAxisDirection 
        + originalPixelLocation.y * yAxisDirection
        + zoomFactor * zAxisDirection);
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
    vec2 mouseLocation = iMouse.xy / iResolution.y;
    
    // some adjustments to make the mouse control a bit less painful
    mouseLocation.y = 0.42 * mouseLocation.y + 0.9 * (1.0 - mouseLocation.y);  // clamp(mouseLocation.y, 0.42, 0.9);
    
    // start from black canvas
    vec3 pixelColor = vec3(0);
    
    // camera is at x=0, y=1, z=0
    vec3 cameraPosition = vec3(0., 0., -3.);
    // moving mouse along y axis rotates around x axis
    // moving mouse down rotates camera position in clockwise direction when looking in the direction of x-axis
    cameraPosition.yz *= RotationMatrix(-mouseLocation.y * 2.0 * PI + 1.0);
    // moving mouse along x axis rotates around y axis
    // moving mouse left rotates camera position in clockwise direction when looking in the direction of y-axis
    cameraPosition.xz *= RotationMatrix(-mouseLocation.x * 1.1 * PI);

    // imagine if camera was at origin and the shader screen was 
    // parallel to xy plane and centered at x=0, y=0, z=1
    // then the vector from camera (origin) to the pixel would be
    // the direction of the ray corresponding to that pixel
    // x is negative to account for x-axis being to the left isntead of right
    vec3 rayDirection = GetRayDirection(originalPixelLocation, cameraPosition, vec3(0., 0., 0.), 1.0);

    float distanceToSurface = RayMarch(cameraPosition, rayDirection);

    vec3 pointOnSurface = cameraPosition + rayDirection * distanceToSurface;

    // float diffusedLighting = GetLight(pointOnSurface);
    // pixelColor = vec3(diffusedLighting);

    if (distanceToSurface < MAX_DIST) {
        pixelColor = GetNormal(pointOnSurface) * 0.5 + 0.5;
    }



    outputPixelColor = vec4(pixelColor,1.0);
}