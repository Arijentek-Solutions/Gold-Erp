import {
	g as T,
	a as l,
	b as e,
	n as i,
	t as d,
	f,
	d as h,
	F as m,
	h as g,
	i as w,
	r as c,
	o as a,
} from "./index-CB7xg2j0.js";
const D = { class: "grid grid-cols-12 gap-6 max-w-7xl mx-auto h-[calc(100vh-6rem)]" },
	I = { class: "col-span-12 lg:col-span-8 flex flex-col gap-6 h-full" },
	A = {
		class: "flex-1 flex flex-col items-center justify-center py-2 glass-card rounded-[2rem] border border-white/5 relative bg-gradient-to-b from-white/5 to-transparent overflow-visible",
	},
	O = { class: "relative group z-10 scale-100" },
	M = {
		class: "w-[380px] h-[380px] rounded-full metallic-bezel border-[4px] border-[#2a2a2a] flex items-center justify-center relative p-1 shadow-[0_0_60px_rgba(0,0,0,0.8)]",
	},
	P = {
		class: "w-full h-full rounded-full border-[10px] border-[#0a0c1a] shadow-inner flex items-center justify-center relative bg-[#05070a]",
	},
	V = {
		class: "w-full h-full rounded-full flex flex-col items-center justify-center relative overflow-hidden bg-[radial-gradient(circle_at_center,_#1a1d2d_0%,_#05070a_70%)]",
	},
	z = { key: 0, class: "absolute bottom-[22%] flex gap-3" },
	F = { class: "mt-8 flex gap-4 w-full max-w-sm z-10" },
	N = ["disabled"],
	R = ["disabled"],
	B = { class: "col-span-12 lg:col-span-4 flex flex-col gap-6 h-full" },
	J = { class: "glass-card rounded-[2rem] p-6 h-1/2 border border-white/10 flex flex-col" },
	K = { class: "flex-1 overflow-y-auto custom-scrollbar space-y-4 pr-2" },
	L = { class: "material-symbols-outlined text-[16px]" },
	Y = {
		class: "text-xs font-bold text-white transition-colors group-hover:text-primary leading-snug",
	},
	$ = { class: "text-[9px] text-white/30 mt-0.5" },
	q = { class: "glass-card rounded-[2rem] p-6 h-1/2 border border-white/10 flex flex-col" },
	E = { class: "flex-1 overflow-y-auto custom-scrollbar space-y-2 pr-2" },
	W = { class: "flex-1 min-w-0" },
	G = {
		class: "text-xs font-medium text-white group-hover:text-primary/90 transition-colors truncate",
	},
	H = { class: "flex items-center gap-2 mt-0.5" },
	U = { class: "text-[9px] text-white/30" },
	Q = { key: 0, class: "w-1.5 h-1.5 rounded-full bg-red-400" },
	ee = {
		__name: "DashboardView",
		setup(X) {
			const r = c(!1),
				b = c("00:00:00"),
				n = c(!1),
				o = c(0);
			let u;
			const p = c([
					{
						id: 1,
						title: "Clock Out",
						time: "Yesterday, 6:00 PM",
						icon: "check_circle",
						type: "clock-out",
					},
					{
						id: 3,
						title: "Clocked In",
						time: "Yesterday, 9:02 AM",
						icon: "login",
						type: "info",
					},
				]),
				y = c([
					{ id: 1, text: "Review diamond inventory", due: "Today, 2:00 PM", urgent: !0 },
					{ id: 2, text: "Submit weekly report", due: "Tomorrow", urgent: !1 },
					{ id: 3, text: "Call with design team", due: "Oct 25", urgent: !1 },
					{ id: 4, text: "Approve pending leaves", due: "Oct 26", urgent: !1 },
					{ id: 5, text: "Check safety gear", due: "Oct 27", urgent: !1 },
				]),
				_ = w(() =>
					r.value
						? o.value >= 28800
							? "text-green-500"
							: "text-red-500"
						: "text-white/20"
				),
				x = w(() => (o.value >= 28800 ? "bg-green-500" : "bg-red-500"));
			function k() {
				(n.value = !0),
					setTimeout(() => {
						(r.value = !0),
							(o.value = 0),
							(n.value = !1),
							p.value.unshift({
								id: Date.now(),
								title: "Clocked In",
								time: "Just now",
								icon: "login",
								type: "info",
							}),
							C();
					}, 800);
			}
			function j() {
				(n.value = !0),
					setTimeout(() => {
						(r.value = !1),
							(n.value = !1),
							p.value.unshift({
								id: Date.now(),
								title: "Clocked Out",
								time: "Just now",
								icon: "logout",
								type: "clock-out",
							}),
							S();
					}, 800);
			}
			function C() {
				u = setInterval(() => {
					o.value++;
					const v = Math.floor(o.value / 3600)
							.toString()
							.padStart(2, "0"),
						t = Math.floor((o.value % 3600) / 60)
							.toString()
							.padStart(2, "0"),
						s = (o.value % 60).toString().padStart(2, "0");
					b.value = `${v}:${t}:${s}`;
				}, 1e3);
			}
			function S() {
				clearInterval(u);
			}
			return (
				T(() => {
					clearInterval(u);
				}),
				(v, t) => (
					a(),
					l("div", D, [
						e("div", I, [
							e("div", A, [
								t[3] ||
									(t[3] = e(
										"div",
										{
											class: "absolute top-0 left-0 w-full h-full diamond-pattern opacity-30 pointer-events-none rounded-[2rem] overflow-hidden",
										},
										null,
										-1
									)),
								t[4] ||
									(t[4] = e(
										"div",
										{
											class: "absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-black/40 pointer-events-none rounded-[2rem]",
										},
										null,
										-1
									)),
								e("div", O, [
									e("div", M, [
										t[2] ||
											(t[2] = e(
												"div",
												{
													class: "absolute inset-0 rounded-full border border-primary/20 shadow-[0_0_40px_rgba(252,211,77,0.1)]",
												},
												null,
												-1
											)),
										e("div", P, [
											e("div", V, [
												t[0] ||
													(t[0] = e(
														"div",
														{
															class: "absolute inset-0 opacity-10",
															style: {
																"background-image": `radial-gradient(
											#fff 1px,
											transparent 1px
										)`,
																"background-size": "20px 20px",
															},
														},
														null,
														-1
													)),
												t[1] ||
													(t[1] = e(
														"div",
														{
															class: "absolute top-[22%] text-[10px] text-white/30 tracking-[0.4em] font-bold uppercase font-display",
														},
														" Current Shift ",
														-1
													)),
												e(
													"div",
													{
														class: i([
															"text-[4.5rem] leading-none font-mono font-bold tracking-tighter mt-2 transition-colors duration-500 z-10 drop-shadow-2xl tabular-nums",
															_.value,
														]),
													},
													d(r.value ? b.value : "00:00:00"),
													3
												),
												r.value
													? (a(),
													  l("div", z, [
															e(
																"span",
																{
																	class: i([
																		"w-2 h-2 rounded-full animate-pulse shadow-[0_0_10px_currentColor]",
																		x.value,
																	]),
																},
																null,
																2
															),
															e(
																"span",
																{
																	class: i([
																		"w-2 h-2 rounded-full opacity-30",
																		x.value,
																	]),
																},
																null,
																2
															),
															e(
																"span",
																{
																	class: i([
																		"w-2 h-2 rounded-full opacity-20",
																		x.value,
																	]),
																},
																null,
																2
															),
													  ]))
													: f("", !0),
											]),
										]),
									]),
								]),
								e("div", F, [
									e(
										"button",
										{
											onClick: k,
											disabled: r.value || n.value,
											class: i([
												"flex-1 h-14 rounded-xl flex items-center justify-center gap-2 transition-all relative font-bold tracking-widest text-sm uppercase",
												[
													r.value
														? "bg-white/5 border border-white/5 text-white/20 cursor-not-allowed"
														: "bg-[#FCD34D] text-black hover:bg-[#FDE047] hover:scale-[1.02] shadow-[0_0_30px_rgba(252,211,77,0.3)]",
												],
											]),
										},
										" Clock In ",
										10,
										N
									),
									e(
										"button",
										{
											onClick: j,
											disabled: !r.value || n.value,
											class: i([
												"flex-1 h-14 rounded-xl flex items-center justify-center gap-2 transition-all relative font-bold tracking-widest text-sm uppercase",
												[
													r.value
														? "bg-[#1a1a1a] border border-white/10 text-white hover:bg-[#252525] hover:border-white/20 hover:text-red-400 shadow-lg"
														: "bg-white/5 border border-white/5 text-white/20 cursor-not-allowed",
												],
											]),
										},
										" Clock Out ",
										10,
										R
									),
								]),
							]),
							t[5] ||
								(t[5] = h(
									'<div class="grid grid-cols-3 gap-6 shrink-0 h-72"><div class="glass-card rounded-2xl p-5 border border-white/5 flex flex-col justify-between relative overflow-hidden group hover:border-white/10 transition-colors"><div class="absolute top-0 right-0 p-3 opacity-5 group-hover:opacity-10 transition-opacity"><span class="material-symbols-outlined text-6xl">badge</span></div><div><p class="text-[10px] text-white/40 font-bold uppercase tracking-wider mb-1"> My Profile </p><div class="flex items-center gap-3 mt-1"><div class="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-orange-500 flex items-center justify-center text-black font-bold text-sm shadow-lg shadow-primary/20"> AW </div><div><p class="text-sm font-bold text-white leading-tight"> Alexander Wright </p><p class="text-[10px] text-primary mt-0.5">Senior Jeweler</p></div></div></div><button class="mt-2 py-2 px-3 bg-white/5 hover:bg-white/10 rounded-lg text-[10px] font-bold text-white border border-white/5 flex items-center gap-2 w-full justify-center transition-all group-hover:bg-white/10"><span class="material-symbols-outlined text-[14px]">account_box</span> View Profile </button></div><div class="glass-card rounded-2xl p-5 border border-white/5 flex flex-col justify-between relative overflow-hidden group hover:border-white/10 transition-colors"><div class="absolute top-0 right-0 p-3 opacity-5 group-hover:opacity-10 transition-opacity"><span class="material-symbols-outlined text-6xl">supervisor_account</span></div><div><p class="text-[10px] text-white/40 font-bold uppercase tracking-wider mb-1"> Reporting To </p><div class="flex items-center gap-3 mt-2"><div class="w-10 h-10 rounded-full bg-blue-500/20 flex items-center justify-center text-blue-400 font-bold text-xs ring-1 ring-blue-500/30"> RK </div><div><p class="text-sm font-bold text-white">Rajesh Kumar</p><p class="text-[10px] text-white/50">Production Head</p></div></div></div><button class="mt-auto py-2 px-3 bg-white/5 hover:bg-white/10 rounded-lg text-[10px] font-bold text-white/70 border border-white/5 w-full transition-all"> View Team </button></div><div class="glass-card rounded-2xl p-5 border border-white/5 flex flex-col justify-between relative overflow-hidden group hover:border-white/10 transition-colors"><div class="absolute top-0 right-0 p-3 opacity-5 group-hover:opacity-10 transition-opacity"><span class="material-symbols-outlined text-6xl">payments</span></div><div><p class="text-[10px] text-white/40 font-bold uppercase tracking-wider mb-1"> Payroll </p><p class="text-base font-bold text-white">Oct 2023</p><p class="text-[10px] text-emerald-400 mt-1 flex items-center gap-1 bg-emerald-400/10 w-fit px-1.5 py-0.5 rounded"><span class="material-symbols-outlined text-[10px]">check_circle</span> Paid </p></div><button class="mt-4 py-2 px-3 bg-primary/10 hover:bg-primary/20 rounded-lg text-[10px] font-bold text-primary border border-primary/20 flex items-center justify-center gap-2 w-full transition-all"><span class="material-symbols-outlined text-[14px]">visibility</span> View Slip </button></div></div>',
									1
								)),
						]),
						e("div", B, [
							e("div", J, [
								t[7] ||
									(t[7] = e(
										"div",
										{ class: "flex items-center justify-between mb-4" },
										[
											e(
												"h3",
												{
													class: "font-bold text-lg text-white font-display",
												},
												"Activity & Alerts"
											),
											e("span", {
												class: "w-2 h-2 bg-primary rounded-full animate-pulse shadow-[0_0_8px_#FCD34D]",
											}),
										],
										-1
									)),
								e("div", K, [
									t[6] ||
										(t[6] = h(
											'<div class="flex gap-3 relative group"><div class="w-8 h-8 rounded-full bg-blue-500/10 flex items-center justify-center shrink-0 border border-blue-500/20 text-blue-400"><span class="material-symbols-outlined text-[16px]">assignment_turned_in</span></div><div><p class="text-xs font-bold text-white leading-snug group-hover:text-blue-400 transition-colors"> New Task Assigned </p><p class="text-[10px] text-white/40 mt-0.5"> &quot;Gemstone Inventory Check&quot; assigned by Rajesh K. </p><p class="text-[9px] text-white/20 mt-1">2 mins ago</p></div></div><div class="flex gap-3 relative group"><div class="w-8 h-8 rounded-full bg-emerald-500/10 flex items-center justify-center shrink-0 border border-emerald-500/20 text-emerald-400"><span class="material-symbols-outlined text-[16px]">check_circle</span></div><div><p class="text-xs font-bold text-white leading-snug group-hover:text-emerald-400 transition-colors"> Leave Approved </p><p class="text-[10px] text-white/40 mt-0.5"> Your leave for Nov 14th has been approved. </p><p class="text-[9px] text-white/20 mt-1">1 hour ago</p></div></div>',
											2
										)),
									(a(!0),
									l(
										m,
										null,
										g(
											p.value,
											(s) => (
												a(),
												l(
													"div",
													{
														key: s.id,
														class: "flex gap-3 relative group opacity-60 hover:opacity-100 transition-opacity",
													},
													[
														e(
															"div",
															{
																class: i([
																	"w-8 h-8 rounded-full flex items-center justify-center shrink-0 border bg-[#0a0c1a]",
																	s.type === "clock-out"
																		? "border-primary/50 text-primary"
																		: "border-white/10 text-white/40",
																]),
															},
															[e("span", L, d(s.icon), 1)],
															2
														),
														e("div", null, [
															e("p", Y, d(s.title), 1),
															e("p", $, d(s.time), 1),
														]),
													]
												)
											)
										),
										128
									)),
								]),
							]),
							e("div", q, [
								t[9] ||
									(t[9] = e(
										"div",
										{ class: "flex items-center justify-between mb-4" },
										[
											e(
												"h3",
												{
													class: "font-bold text-lg text-white font-display",
												},
												"My Tasks"
											),
											e(
												"button",
												{
													class: "w-6 h-6 rounded-full bg-white/5 hover:bg-white/10 flex items-center justify-center text-white/50 hover:text-white transition-all border border-white/5",
												},
												[
													e(
														"span",
														{
															class: "material-symbols-outlined text-[16px]",
														},
														"add"
													),
												]
											),
										],
										-1
									)),
								e("div", E, [
									(a(!0),
									l(
										m,
										null,
										g(
											y.value,
											(s) => (
												a(),
												l(
													"div",
													{
														key: s.id,
														class: "group flex items-center gap-3 p-3 rounded-xl hover:bg-white/5 transition-all border border-transparent hover:border-white/5 cursor-pointer",
													},
													[
														t[8] ||
															(t[8] = e(
																"div",
																{
																	class: "w-4 h-4 rounded border border-white/20 flex items-center justify-center group-hover:border-primary transition-colors text-transparent group-hover:text-white/20",
																},
																[
																	e(
																		"span",
																		{
																			class: "material-symbols-outlined text-[12px]",
																		},
																		"check"
																	),
																],
																-1
															)),
														e("div", W, [
															e("p", G, d(s.text), 1),
															e("div", H, [
																e("span", U, d(s.due), 1),
																s.urgent
																	? (a(), l("span", Q))
																	: f("", !0),
															]),
														]),
													]
												)
											)
										),
										128
									)),
								]),
							]),
						]),
					])
				)
			);
		},
	};
export { ee as default };
