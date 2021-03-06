var ANG2RAD = 3.14159265358979323846/180.0;

function FrustumCulling(){
	this.updatePlanes();
}

/* Crea un piano a partire da tre punti nello spazio. Restituisce un array di quattro componenti [A,B,C,D] dove Ax + By + Cz + D = 0 */
FrustumCulling.prototype.createPlane = function(p0, p1, p2) {
	var v = p1.sub(p0);
	var u = p2.sub(p0);
	var n = v.cross(u);
	n.$unit();
	var A = n.x;
	var B = n.y;
	var C = n.z;
	var D = n.neg().dot(p0);

	return [A,B,C,D];
}

/* Controlla che un punto sia all'interno del piano, torna true o false */
FrustumCulling.prototype.isPointInFrustum = function(point){
	return this.isSphereInFrustum(point, 0);
}

/* Controlla che una sfera sia all'interno del piano (dato il centro ed il raggio della sfera), torna true o false */
FrustumCulling.prototype.isSphereInFrustum = function(point, radius){
	for(var key in this.planes){
		var plane = this.planes[key];
		var dist = this.distToPlane(plane, point);
		if(dist < -radius*2){
			return false;
		}
	}
	return true;
}

/* Calcola la distanza di un punto dal piano */
FrustumCulling.prototype.distToPlane = function(plane, point) {
	var A = plane[0], B = plane[1], C = plane[2], D = plane[3];
	var rx = point.x, ry = point.y, rz = point.z;

	var dist = A*rx + B*ry + C*rz + D;

	return dist;
}

/* Aggiorna i sei piani che identificano la frustum della camera (volume che determina lo spazio in cui gli oggetti vengono visualizzati)
   imposta una variabile di classe planes che è un mappa contenente i sei piani della frustum */
FrustumCulling.prototype.updatePlanes = function(p, l, u){
	var dir,nc,fc,X,Y,Z;

	this.ratio = camera.aspect;
	this.angle = camera.fov;
	this.nearD = camera.near;
	this.farD = camera.far;

	var tang = Math.tan(ANG2RAD * this.angle * 0.5) ;

	this.nh = this.nearD * tang;
	this.nw = this.nh * this.ratio;
	this.fh = this.farD * tang;
	this.fw = this.fh * this.ratio;

	if(p!=undefined && l!=undefined && u!=undefined){
		Z = p.sub(l);
		Z.$unit();

		X = u.cross(Z);
		X.$unit();

		Y = Z.cross(X);

		nc = p.sub(Z.scale(this.nearD));
		fc = p.sub(Z.scale(this.farD));

		function computeCorners(c, h, w){
			var tl = c.add(Y.scale(h)).sub(X.scale(w)),
			tr = c.add(Y.scale(h)).add(X.scale(w)),
			bl = c.sub(Y.scale(h)).sub(X.scale(w)),
			br = c.sub(Y.scale(h)).add(X.scale(w));
			return [tl,tr,bl,br];
		}

		n = computeCorners(nc, this.nh, this.nw);
		f = computeCorners(fc, this.fh, this.fw);
		var ntl = n[0], ntr = n[1], nbl = n[2], nbr = n[3];
		var ftl = f[0], ftr = f[1], fbl = f[2], fbr = f[3];

		var planes = {};

		planes['TOP'] = this.createPlane(ntr,ntl,ftl);
		planes['BOTTOM'] = this.createPlane(nbl,nbr,fbr);
		planes['LEFT'] = this.createPlane(ntl,nbl,fbl);
		planes['RIGHT'] = this.createPlane(nbr,ntr,fbr);
		planes['NEAR'] = this.createPlane(ntl,ntr,nbr);
		planes['FAR'] = this.createPlane(ftr,ftl,fbl);

		this.planes = planes;
	}
}