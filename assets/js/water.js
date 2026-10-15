/* Calm water caustics behind dark heroes. WebGL, low resolution, paused when off screen. */
(function () {
  var canvases = document.querySelectorAll("canvas.water");
  if (!canvases.length) return;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var VERT = "attribute vec2 p;void main(){gl_Position=vec4(p,0.0,1.0);}";
  var FRAG = [
    "precision mediump float;",
    "uniform vec2 uRes;",
    "uniform float uTime;",
    "uniform vec2 uMouse;",
    "uniform float uHover;",
    "vec2 hash2(vec2 p){p=vec2(dot(p,vec2(127.1,311.7)),dot(p,vec2(269.5,183.3)));return fract(sin(p)*43758.5453);}",
    "float cells(vec2 x,float t){",
    "  vec2 n=floor(x);vec2 f=fract(x);float d1=8.0;float d2=8.0;",
    "  for(int j=-1;j<=1;j++){for(int i=-1;i<=1;i++){",
    "    vec2 g=vec2(float(i),float(j));vec2 o=hash2(n+g);",
    "    o=0.5+0.45*sin(t+6.2831*o);",
    "    vec2 r=g+o-f;float d=dot(r,r);",
    "    if(d<d1){d2=d1;d1=d;}else if(d<d2){d2=d;}",
    "  }}",
    "  return sqrt(d2)-sqrt(d1);",
    "}",
    "void main(){",
    "  vec2 uv=gl_FragCoord.xy/uRes;",
    "  float s=min(uRes.x,uRes.y);",
    "  vec2 p=gl_FragCoord.xy/s;",
    "  vec2 m=uMouse/s;",
    "  float dm=length(p-m);",
    "  float ripple=uHover*sin(dm*30.0-uTime*3.2)*exp(-dm*5.0)*0.04;",
    "  p+=normalize(p-m+0.0001)*ripple;",
    "  float t=uTime*0.32;",
    "  vec2 w=p*2.4;",
    "  w+=vec2(sin(w.y*1.3+t*1.1),cos(w.x*1.1-t*0.9))*0.55;",
    "  w+=vec2(sin(w.y*2.3-t*0.7),cos(w.x*2.1+t*0.8))*0.22;",
    "  float c1=cells(w,t);",
    "  float c2=cells(w*1.9+3.7,t*1.25);",
    "  float caust=pow(1.0-smoothstep(0.0,0.2,c1),2.4)*0.75+pow(1.0-smoothstep(0.0,0.16,c2),2.4)*0.3;",
    "  vec3 deep=vec3(0.028,0.072,0.125);",
    "  vec3 mid=vec3(0.05,0.17,0.26);",
    "  vec3 col=mix(deep,mid,smoothstep(0.0,1.2,uv.y*0.85+uv.x*0.4));",
    "  float glow=exp(-dm*3.2)*uHover;",
    "  float light=caust*(0.05+0.17*smoothstep(0.05,1.0,uv.y*0.7+uv.x*0.5))+glow*caust*0.3;",
    "  col+=vec3(0.42,0.8,0.88)*light;",
    "  col+=vec3(0.9,0.72,0.4)*glow*0.035;",
    "  float vig=smoothstep(1.3,0.2,length(uv-vec2(0.65,0.6)));",
    "  col*=0.72+0.28*vig;",
    "  gl_FragColor=vec4(col,1.0);",
    "}"
  ].join("\n");

  function compile(gl, type, src) {
    var sh = gl.createShader(type);
    gl.shaderSource(sh, src);
    gl.compileShader(sh);
    if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) return null;
    return sh;
  }

  function init(canvas) {
    var gl = canvas.getContext("webgl", { antialias: false, alpha: false, depth: false, powerPreference: "low-power" });
    if (!gl) return;
    var vs = compile(gl, gl.VERTEX_SHADER, VERT);
    var fs = compile(gl, gl.FRAGMENT_SHADER, FRAG);
    if (!vs || !fs) return;
    var prog = gl.createProgram();
    gl.attachShader(prog, vs);
    gl.attachShader(prog, fs);
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) return;
    gl.useProgram(prog);

    var buf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    var loc = gl.getAttribLocation(prog, "p");
    gl.enableVertexAttribArray(loc);
    gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);

    var uRes = gl.getUniformLocation(prog, "uRes");
    var uTime = gl.getUniformLocation(prog, "uTime");
    var uMouse = gl.getUniformLocation(prog, "uMouse");
    var uHover = gl.getUniformLocation(prog, "uHover");

    var w = 1, h = 1, k = 1;
    var mouse = { x: 0, y: 0 }, target = { x: 0, y: 0 };
    var hover = 0, hoverTarget = 0;
    var visible = false, raf = 0, ready = false;
    var start = performance.now(), offset = Math.random() * 50;

    function resize() {
      var r = canvas.getBoundingClientRect();
      var dpr = Math.min(window.devicePixelRatio || 1, 1.5);
      k = dpr * 0.55;
      w = Math.max(1, Math.round(r.width * k));
      h = Math.max(1, Math.round(r.height * k));
      if (canvas.width !== w || canvas.height !== h) {
        canvas.width = w;
        canvas.height = h;
        gl.viewport(0, 0, w, h);
      }
      if (!mouse.x) { mouse.x = target.x = w * 0.7; mouse.y = target.y = h * 0.55; }
    }

    function frame(now) {
      raf = 0;
      if (!visible || document.hidden) return;
      mouse.x += (target.x - mouse.x) * 0.07;
      mouse.y += (target.y - mouse.y) * 0.07;
      hover += (hoverTarget - hover) * 0.04;
      gl.uniform2f(uRes, w, h);
      gl.uniform1f(uTime, offset + (now - start) / 1000);
      gl.uniform2f(uMouse, mouse.x, mouse.y);
      gl.uniform1f(uHover, hover);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
      if (!ready) { ready = true; canvas.classList.add("is-ready"); }
      if (!reduce) raf = requestAnimationFrame(frame);
    }

    function kick() { if (!raf) raf = requestAnimationFrame(frame); }

    var host = canvas.parentElement;
    host.addEventListener("pointermove", function (e) {
      if (e.pointerType !== "mouse") return;
      var r = canvas.getBoundingClientRect();
      target.x = (e.clientX - r.left) * k;
      target.y = (r.bottom - e.clientY) * k;
      hoverTarget = 1;
      if (reduce) kick();
    });
    host.addEventListener("pointerleave", function () { hoverTarget = 0; });

    new IntersectionObserver(function (entries) {
      visible = entries[0].isIntersecting;
      if (visible) kick();
    }).observe(canvas);
    document.addEventListener("visibilitychange", kick);
    window.addEventListener("resize", function () { resize(); kick(); });
    resize();
  }

  for (var i = 0; i < canvases.length; i++) init(canvases[i]);
})();
