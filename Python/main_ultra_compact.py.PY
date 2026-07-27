""
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from datetime import datetime
import logging

from literature_search_engine import LiteratureSearchEngine
from user_profile_manager import UserProfileManager
from skill_assessment import SkillAssessmentEngine
from note_window import NoteWindow
from ui_components import SearchResultFrame, PaginationFrame
from personalization_form import PersonalizationFormWindow
from skill_dashboard import SkillDashboardWindow
from game_hub import GameHubWindow

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Config:
    """Configuration"""
    WINDOW_TITLE = "AI Literature & Skill Development"
    WINDOW_SIZE, WINDOW_MIN_SIZE = (1400, 950), (1200, 750)
    SIDEBAR_WIDTH, RESULTS_PER_PAGE, PADDING = 250, 10, 10
    FONTS = {'title': ("Arial", 16, "bold"), 'subtitle': ("Arial", 14, "bold"), 'label': ("Arial", 11, "bold"),
             'normal': ("Arial", 10), 'small': ("Arial", 9), 'tiny': ("Arial", 8)}
    SKILLS = ['Self-Confidence', 'Research', 'Analysis', 'Communication']
    ACHIEVEMENTS = {
        'first_search': ('🔍 First Search', 10, 'Perform first search'),
        'five_searches': ('🔥 Search Master', 50, 'Perform 5 searches'),
        'ten_notes': ('📝 Note Taker', 100, 'Create 10 notes'),
        'skill_50': ('⭐ Rising Star', 100, 'Reach 50+ skill score'),
        'skill_80': ('🏆 Expert', 250, 'Reach 80+ skill score'),
        'complete_profile': ('👤 Profile Master', 25, 'Complete profile'),
        'assessment': ('📊 Assessor', 50, 'Complete skill assessment'),
        'game_win': ('🎮 Game Winner', 75, 'Win a game'),
    }
    POINTS, LEADERBOARD = {'search': 10, 'note': 15, 'assessment': 50}, [
        ("Alex Chen", 5230, 53), ("Maria Garcia", 4890, 49), ("James Wilson", 4560, 46), ("Emma Davis", 4120, 42)]
    CHALLENGES = [
        {"title": "Search Master", "desc": "Perform 5 searches today", "reward": "50 pts"},
        {"title": "Note Creator", "desc": "Create 3 notes", "reward": "45 pts"},
        {"title": "Skill Booster", "desc": "Reach 50+ in any skill", "reward": "100 pts"},
        {"title": "Game Winner", "desc": "Win a game with 70+ score", "reward": "75 pts"},
    ]


class Gamification:
    """Gamification system"""
    def __init__(self, pm):
        try:
            self.pm, self.p = pm, pm.load_profile() or pm.create_default_profile()
            if 'gamification' not in self.p:
                self.p['gamification'] = {'total_points': 0, 'level': 1, 'achievements': [], 'searches': 0, 'notes_created': 0, 'games_played': 0, 'last_activity': None}
                self._save()
            logger.info("✅ Gamification initialized")
        except Exception as e:
            logger.error(f"❌ Gamification init: {e}"), raise
    
    def add_points(self, pts, action):
        self.p['gamification']['total_points'] += pts
        self.p['gamification']['level'] = 1 + (self.p['gamification']['total_points'] // 100)
        self._save()
        return self.p['gamification']['total_points']
    
    def unlock(self, key):
        if key in Config.ACHIEVEMENTS and key not in self.p['gamification']['achievements']:
            self.p['gamification']['achievements'].append(key)
            self.add_points(Config.ACHIEVEMENTS[key][1], 'achievement')
            logger.info(f"🏆 {Config.ACHIEVEMENTS[key][0]}")
            return True
        return False
    
    def _save(self):
        try: self.pm.save_profile(self.p)
        except Exception as e: logger.error(f"Save failed: {e}")
    
    def get_stats(self): return self.p['gamification']
    def get_next_pts(self): return max(0, self.p['gamification']['level'] * 100 - self.p['gamification']['total_points'])
    def track_search(self):
        self.p['gamification']['searches'] += 1
        self.add_points(Config.POINTS['search'], 'search')
        if self.p['gamification']['searches'] == 1: self.unlock('first_search')
        elif self.p['gamification']['searches'] == 5: self.unlock('five_searches')
    def track_note(self):
        self.p['gamification']['notes_created'] += 1
        self.add_points(Config.POINTS['note'], 'note')
        if self.p['gamification']['notes_created'] == 10: self.unlock('ten_notes')
    def track_game(self, s):
        self.p['gamification']['games_played'] += 1
        self.add_points(int(s / 10), 'game')
        if s >= 70: self.unlock('game_win')


class UI:
    """UI Builder"""
    @staticmethod
    def lbl(p, t, f='normal', **kw): return ttk.Label(p, text=t, font=Config.FONTS.get(f, f), **kw)
    @staticmethod
    def btn(p, t, c, **kw): return ttk.Button(p, text=t, command=c, **kw)
    @staticmethod
    def ent(p, v, **kw): return ttk.Entry(p, textvariable=v, font=Config.FONTS['normal'], **kw)
    @staticmethod
    def prg(p, v=0, **kw): return ttk.Progressbar(p, mode='determinate', value=v, **kw)
    @staticmethod
    def frm(p, w=None, **kw):
        f = ttk.Frame(p, **kw)
        if w: f.pack_propagate(False), f.configure(width=w)
        return f
    @staticmethod
    def lfrm(p, t, **kw): return ttk.LabelFrame(p, text=t, **kw)


class App:
    """Main Application"""
    def __init__(self, root):
        try:
            self.root = root
            self.root.title(Config.WINDOW_TITLE)
            self.root.geometry(f"{Config.WINDOW_SIZE[0]}x{Config.WINDOW_SIZE[1]}")
            self.root.minsize(*Config.WINDOW_MIN_SIZE)
            ttk.Style().theme_use('clam')
            
            self.se, self.pm, self.sa = LiteratureSearchEngine(), UserProfileManager(), SkillAssessmentEngine()
            self.gam = Gamification(self.pm)
            self.results, self.page, self.total_pages, self.keyword, self.notes, self.up = [], 0, 0, "", {}, self.pm.load_profile()
            self.skill_labels, self.ach_win = {}, None
            
            self._menu()
            self._build()
            
            if not self.up or not self.up.get('name'):
                messagebox.showinfo("Welcome", "Complete your profile first!")
                self.profile()
            logger.info("✅ App initialized")
        except Exception as e:
            logger.error(f"❌ Init: {e}"), messagebox.showerror("Error", f"Failed: {e}")
    
    def _menu(self):
        mb = tk.Menu(self.root)
        self.root.config(menu=mb)
        fm = tk.Menu(mb, tearoff=0)
        mb.add_cascade(label="📄 File", menu=fm)
        fm.add_command(label="Profile", command=self.profile)
        fm.add_command(label="Exit", command=self.root.quit)
        dm = tk.Menu(mb, tearoff=0)
        mb.add_cascade(label="🎓 Dev", menu=dm)
        dm.add_command(label="Skills", command=self.skills_dash)
        dm.add_command(label="Games", command=self.games)
        gm = tk.Menu(mb, tearoff=0)
        mb.add_cascade(label="🏆 Game", menu=gm)
        gm.add_command(label="Achievements", command=self.achievements)
        gm.add_command(label="Leaderboard", command=self.leaderboard)
        gm.add_command(label="Challenges", command=self.challenges)
    
    def _build(self):
        m = UI.frm(self.root)
        m.pack(fill=tk.BOTH, expand=True)
        self._left(m)
        self._center(m)
        self._right(m)
    
    def _left(self, p):
        l = UI.frm(p, width=Config.SIDEBAR_WIDTH)
        l.pack(side=tk.LEFT, fill=tk.BOTH, padx=Config.PADDING, pady=Config.PADDING)
        
        gf = UI.lfrm(l, text="🏆 Gamification", padding=Config.PADDING)
        gf.pack(fill=tk.X, pady=(0, 10))
        s = self.gam.get_stats()
        UI.lbl(gf, f"⭐ Level {s['level']}", 'label').pack(anchor=tk.W)
        UI.lbl(gf, f"🎯 Points: {s['total_points']}", 'normal').pack(anchor=tk.W, pady=(5, 0))
        UI.lbl(gf, f"Next: {self.gam.get_next_pts()} pts", 'tiny').pack(anchor=tk.W)
        prg = UI.prg(gf, value=min(100, s['total_points'] % 100), length=220)
        prg.pack(fill=tk.X, pady=5)
        UI.lbl(gf, f"🔍 Searches: {s['searches']}", 'tiny').pack(anchor=tk.W)
        UI.lbl(gf, f"📝 Notes: {s['notes_created']}", 'tiny').pack(anchor=tk.W)
        UI.lbl(gf, f"🎮 Games: {s['games_played']}", 'tiny').pack(anchor=tk.W)
        UI.lbl(gf, f"🏅 Achievements: {len(s['achievements'])}/{len(Config.ACHIEVEMENTS)}", ('Arial', 8, 'bold')).pack(anchor=tk.W, pady=(5, 0))
        
        pf = UI.lfrm(l, text="👤 Profile", padding=Config.PADDING)
        pf.pack(fill=tk.X, pady=(0, 10))
        if self.up and self.up.get('name'):
            UI.lbl(pf, f"👤 {self.up['name']}", 'label').pack(anchor=tk.W)
            UI.lbl(pf, f"Goal: {self.up.get('goal', 'N/A')}", 'small', wraplength=200).pack(anchor=tk.W)
        UI.btn(pf, "✏️ Edit Profile", self.profile).pack(fill=tk.X, pady=5)
        
        sf = UI.lfrm(l, text="📊 Your Skills", padding=Config.PADDING)
        sf.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        for skill in Config.SKILLS:
            sr = UI.frm(sf)
            sr.pack(fill=tk.X, pady=5)
            UI.lbl(sr, skill, 'small').pack(anchor=tk.W)
            sc = self._skill_score(skill)
            pg = UI.prg(sr, value=sc, length=220)
            pg.pack(fill=tk.X, pady=2)
            lb = UI.lbl(sr, f"{sc}/100", ('Arial', 8, 'bold'))
            lb.pack(anchor=tk.W)
            self.skill_labels[skill] = (pg, lb)
        
        af = UI.lfrm(l, text="⚡ Actions", padding=Config.PADDING)
        af.pack(fill=tk.X)
        UI.btn(af, "📊 Skills", self.skills_dash).pack(fill=tk.X, pady=3)
        UI.btn(af, "🎮 Games", self.games).pack(fill=tk.X, pady=3)
        UI.btn(af, "📝 Notes", self.my_notes).pack(fill=tk.X, pady=3)
        UI.btn(af, "🏆 Achievements", self.achievements).pack(fill=tk.X, pady=3)
    
    def _center(self, p):
        c = UI.frm(p)
        c.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=Config.PADDING, pady=Config.PADDING)
        
        UI.lbl(c, "📚 Search Literature", 'subtitle').pack(anchor=tk.W, pady=(0, 10))
        
        sf = UI.frm(c)
        sf.pack(fill=tk.X, pady=(0, 5))
        self.search_var = tk.StringVar()
        e = UI.ent(sf, self.search_var, width=50)
        e.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        e.bind("<Return>", lambda e: self.search())
        UI.btn(sf, "🔍 Search", self.search).pack(side=tk.LEFT, padx=5)
        
        self.status_lbl = UI.lbl(c, "Ready to search", relief=tk.SUNKEN, font='small')
        self.status_lbl.pack(fill=tk.X, pady=5)
        
        rc = UI.frm(c)
        rc.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        sb = ttk.Scrollbar(rc)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas = tk.Canvas(rc, yscrollcommand=sb.set, bg="white", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.config(command=self.canvas.yview)
        
        self.res_frm = UI.frm(self.canvas)
        self.canvas_win = self.canvas.create_window((0, 0), window=self.res_frm, anchor="nw")
        self.res_frm.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.pag_frm = PaginationFrame(c, on_previous=self.prev_page, on_next=self.next_page, on_page_select=self.go_page)
        self.pag_frm.pack(fill=tk.X, pady=10)
        self.pag_frm.pack_forget()
    
    def _right(self, p):
        r = UI.frm(p, width=Config.SIDEBAR_WIDTH)
        r.pack(side=tk.RIGHT, fill=tk.BOTH, padx=Config.PADDING, pady=Config.PADDING)
        
        rf = UI.lfrm(r, text="🎯 Recommendations", padding=Config.PADDING)
        rf.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        if self.up and self.up.get('interests'):
            for i in self.up.get('interests', [])[:3]:
                UI.btn(rf, f"🔍 {i}", lambda x=i: self.search_kw(x)).pack(fill=tk.X, pady=3)
        else:
            UI.lbl(rf, "Complete profile\nfor recommendations", 'small', justify=tk.CENTER).pack(pady=20)
        
        pf = UI.lfrm(r, text="📈 Learning Path", padding=Config.PADDING)
        pf.pack(fill=tk.X, pady=(0, 10))
        UI.lbl(pf, "Current Goal:", ('Arial', 9, 'bold')).pack(anchor=tk.W)
        if self.up and self.up.get('goal'):
            UI.lbl(pf, self.up['goal'], 'tiny', wraplength=220).pack(anchor=tk.W, pady=5)
        pg = UI.prg(pf, value=45, length=220)
        pg.pack(fill=tk.X, pady=5)
        UI.lbl(pf, "45% Complete", 'tiny').pack(anchor=tk.W)
        
        nf = UI.lfrm(r, text="📖 Recent Notes", padding=Config.PADDING)
        nf.pack(fill=tk.BOTH, expand=True)
        if self.notes:
            for nid, nd in list(self.notes.items())[-3:]:
                t = nd.get('paper', {}).get('title', 'Untitled')[:30]
                UI.btn(nf, f"• {t}...", lambda: None).pack(fill=tk.X, pady=2)
        else:
            UI.lbl(nf, "No notes yet.\nStart searching!", 'small', justify=tk.CENTER).pack(pady=30)
    
    def profile(self):
        try:
            PersonalizationFormWindow(self.root, self.pm, self._prof_update)
            self.gam.unlock('complete_profile')
        except Exception as e:
            logger.error(f"Profile: {e}"), messagebox.showerror("Error", "Profile failed")
    
    def _prof_update(self):
        try:
            self.up = self.pm.load_profile()
            self._skill_update()
        except Exception as e:
            logger.error(f"Profile update: {e}")
    
    def _skill_score(self, sn):
        try:
            return self.up['skills'].get(sn, 0) if self.up and 'skills' in self.up else 0
        except:
            return 0
    
    def _skill_update(self):
        try:
            for sn, (pg, lb) in self.skill_labels.items():
                sc = self._skill_score(sn)
                pg.config(value=sc)
                lb.config(text=f"{sc}/100")
        except Exception as e:
            logger.error(f"Skill update: {e}")
    
    def skills_dash(self):
        try:
            SkillDashboardWindow(self.root, self.pm, self.sa, self._prof_update)
        except Exception as e:
            logger.error(f"Skills: {e}"), messagebox.showerror("Error", "Skills failed")
    
    def games(self):
        try:
            GameHubWindow(self.root, self.pm, self.sa, self._prof_update)
        except Exception as e:
            logger.error(f"Games: {e}"), messagebox.showerror("Error", "Games failed")
    
    def search(self):
        try:
            kw = self.search_var.get().strip()
            if not kw:
                messagebox.showwarning("Error", "Enter keyword")
                return
            self.search_kw(kw)
        except Exception as e:
            logger.error(f"Search: {e}"), messagebox.showerror("Error", str(e))
    
    def search_kw(self, kw):
        """Background search - NO UI FREEZING"""
        try:
            self.keyword, self.page = kw, 0
            self.search_var.set(kw)
            self.status_lbl.config(text="🔍 Searching...")
            self.gam.track_search()
            t = threading.Thread(target=self._search_bg, args=(kw,), daemon=True)
            t.start()
        except Exception as e:
            logger.error(f"Search kw: {e}"), self.status_lbl.config(text="❌ Error")
    
    def _search_bg(self, kw):
        """Background thread - PRESERVES RESPONSIVENESS"""
        try:
            self.results = self.se.search(kw, self.up)
            self.total_pages = (len(self.results) + Config.RESULTS_PER_PAGE - 1) // Config.RESULTS_PER_PAGE
            self.root.after(0, self.display)
            self.root.after(0, lambda: self.status_lbl.config(text=f"✅ Found {len(self.results)} results ({self.total_pages} pages)"))
            logger.info(f"✅ Search: {len(self.results)} for '{kw}'")
        except Exception as e:
            logger.error(f"Search bg: {e}")
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            self.root.after(0, lambda: self.status_lbl.config(text="❌ Failed"))
    
    def display(self):
        try:
            for w in self.res_frm.winfo_children():
                w.destroy()
            if not self.results:
                UI.lbl(self.res_frm, "No results", 'normal').pack(pady=40)
                self.pag_frm.pack_forget()
                return
            st = self.page * Config.RESULTS_PER_PAGE
            ed = min(st + Config.RESULTS_PER_PAGE, len(self.results))
            for i in range(st, ed):
                rf = SearchResultFrame(self.res_frm, self.results[i], i + 1, on_hover=None, on_add_note=self.note_win)
                rf.pack(fill=tk.X, padx=5, pady=5)
            self.pag_frm.update_pagination(self.page + 1, self.total_pages)
            self.pag_frm.pack(fill=tk.X, pady=10)
        except Exception as e:
            logger.error(f"Display: {e}")
    
    def prev_page(self):
        if self.page > 0:
            self.page -= 1
            self.display()
            self.canvas.yview_moveto(0)
    
    def next_page(self):
        if self.page < self.total_pages - 1:
            self.page += 1
            self.display()
            self.canvas.yview_moveto(0)
    
    def go_page(self, pn):
        if 0 <= pn - 1 < self.total_pages:
            self.page = pn - 1
            self.display()
            self.canvas.yview_moveto(0)
    
    def note_win(self, r):
        try:
            NoteWindow(self.root, r, self.keyword, self.se, self.save_note)
        except Exception as e:
            logger.error(f"Note win: {e}"), messagebox.showerror("Error", "Note failed")
    
    def save_note(self, rid, nc):
        try:
            self.notes[rid] = nc
            self.gam.track_note()
            messagebox.showinfo("Success", "✅ Note saved! +15 pts 🎯")
        except Exception as e:
            logger.error(f"Save note: {e}"), messagebox.showerror("Error", "Save failed")
    
    def my_notes(self):
        try:
            nw = tk.Toplevel(self.root)
            nw.title("📖 My Notes")
            nw.geometry("800x600")
            tf = UI.frm(nw)
            tf.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            sb = ttk.Scrollbar(tf)
            sb.pack(side=tk.RIGHT, fill=tk.Y)
            t = ttk.Treeview(tf, yscrollcommand=sb.set, columns=('Date', 'Keyword'))
            t.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            sb.config(command=t.yview)
            t.heading('#0', text='Paper Title')
            t.heading('Date', text='Date Created')
            t.heading('Keyword', text='Keyword')
            for nid, nd in self.notes.items():
                p = nd.get('paper', {})
                dt = nd.get('timestamp', '')[:10]
                kw = nd.get('keyword', '')
                t.insert('', 'end', text=p.get('title', 'Untitled')[:50], values=(dt, kw))
        except Exception as e:
            logger.error(f"My notes: {e}"), messagebox.showerror("Error", "Notes failed")
    
    def achievements(self):
        try:
            if self.ach_win and self.ach_win.winfo_exists():
                self.ach_win.lift()
                return
            self.ach_win = tk.Toplevel(self.root)
            self.ach_win.title("🏆 Achievements")
            self.ach_win.geometry("600x700")
            s = self.gam.get_stats()
            u = s['achievements']
            UI.lbl(self.ach_win, "🏆 Your Achievements", 'title').pack(pady=20)
            sf = UI.frm(self.ach_win)
            sf.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            sb = ttk.Scrollbar(sf)
            sb.pack(side=tk.RIGHT, fill=tk.Y)
            cv = tk.Canvas(sf, yscrollcommand=sb.set, bg="white")
            cv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            sb.config(command=cv.yview)
            inn = UI.frm(cv)
            cv.create_window((0, 0), window=inn, anchor="nw")
            for k, (nm, pts, ds) in Config.ACHIEVEMENTS.items():
                ul = k in u
                af = UI.lfrm(inn, text=nm, padding=10)
                af.pack(fill=tk.X, pady=10, padx=10)
                st = "✅ UNLOCKED" if ul else "🔒 LOCKED"
                cl = "green" if ul else "red"
                UI.lbl(af, f"{st} | {pts} pts", ('Arial', 10, 'bold'), foreground=cl).pack(anchor=tk.W)
                UI.lbl(af, ds, 'small').pack(anchor=tk.W, pady=(5, 0))
            inn.bind("<Configure>", lambda e: cv.configure(scrollregion=cv.bbox("all")))
        except Exception as e:
            logger.error(f"Achievements: {e}"), messagebox.showerror("Error", "Achievements failed")
    
    def leaderboard(self):
        try:
            lw = tk.Toplevel(self.root)
            lw.title("🏅 Leaderboard")
            lw.geometry("500x500")
            UI.lbl(lw, "🏅 Top Players", 'title').pack(pady=20)
            ud = ("You", self.gam.get_stats()['total_points'], self.gam.get_stats()['level'])
            dt = [ud] + Config.LEADERBOARD
            tf = UI.frm(lw)
            tf.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            t = ttk.Treeview(tf, columns=('Points', 'Level'), height=15)
            t.pack(fill=tk.BOTH, expand=True)
            t.heading('#0', text='Rank - Player')
            t.heading('Points', text='Points')
            t.heading('Level', text='Level')
            for rk, (pl, pts, lv) in enumerate(dt, 1):
                t.insert('', 'end', text=f"{rk}. {pl}", values=(pts, f"Lvl {lv}"))
        except Exception as e:
            logger.error(f"Leaderboard: {e}"), messagebox.showerror("Error", "Leaderboard failed")
    
    def challenges(self):
        try:
            cw = tk.Toplevel(self.root)
            cw.title("⚡ Daily Challenge")
            cw.geometry("500x400")
            UI.lbl(cw, "⚡ Today's Challenge", 'title').pack(pady=20)
            for c in Config.CHALLENGES:
                cf = UI.lfrm(cw, text=c['title'], padding=10)
                cf.pack(fill=tk.X, padx=20, pady=10)
                UI.lbl(cf, c['desc'], 'normal').pack(anchor=tk.W)
                UI.lbl(cf, f"Reward: {c['reward']}", ('Arial', 9, 'bold'), foreground="green").pack(anchor=tk.W, pady=(5, 0))
        except Exception as e:
            logger.error(f"Challenges: {e}"), messagebox.showerror("Error", "Challenges failed")


def main():
    try:
        r = tk.Tk()
        a = App(r)
        r.mainloop()
    except Exception as e:
        logger.error(f"❌ Fatal: {e}"), messagebox.showerror("Fatal", f"Failed: {e}")


if __name__ == "__main__":
    main()
