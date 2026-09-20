// opencode-v2-skills marketplace — browse, install, update, search skills
// Commands: /skill-manager list, /skill-manager install <name>, /skill-manager uninstall <name>, /skill-manager search <term>, /skill-manager update <name>
export default {
  id: "skill-manager",
  async setup(ctx) {
    const SKILLS_REPO = "https://github.com/Joey-1123/opencode-v2-skills.git"
    const SKILLS_DIR = process.env.HOME + "/.config/opencode/skills"
    const CACHE_DIR = "/tmp/skills-cache"
    const execSync = (await import("child_process")).execSync

    // Helper: clone/cache the repo to read SKILL.md files
    async function getCatalog() {
      try {
        execSync(`git clone --depth 1 ${SKILLS_REPO} ${CACHE_DIR} 2>/dev/null || (cd ${CACHE_DIR} && git pull --ff-only 2>/dev/null)`, { stdio: "ignore" })
        const skills = []
        const dirs = execSync(`ls -d ${CACHE_DIR}/skills/*/ 2>/dev/null`).toString().trim().split("\n").filter(Boolean)
        for (const dir of dirs) {
          const name = dir.replace(`${CACHE_DIR}/skills/`, "").replace("/", "")
          const skillMd = `${dir}SKILL.md`
          let desc = ""
          try {
            const content = execSync(`cat "${skillMd}"`, { encoding: "utf-8" })
            const match = content.match(/description:\s*(.+)/)
            if (match) desc = match[1].trim()
          } catch {}
          skills.push({ name, desc })
        }
        return skills
      } catch (e) {
        return []
      }
    }

    // Helper: get installed skills
    function getInstalled() {
      try {
        return execSync(`ls -d ${SKILLS_DIR}/*/ 2>/dev/null`).toString().trim().split("\n").filter(Boolean).map(d => d.replace(`${SKILLS_DIR}/`, "").replace("/", ""))
      } catch { return [] }
    }

    // Command: list all skills with descriptions
    await ctx.command.transform((editor) => {
      editor.add({
        name: "skill-manager-list",
        description: "Browse all skills in the marketplace",
        execute: async ({ sessionID, delivery }) => {
          const catalog = await getCatalog()
          const installed = getInstalled()
          if (catalog.length === 0) {
            await ctx.session.prompt({ sessionID, text: "📭 No skills found. Run /skill-manager install first.", delivery })
            return
          }
          let msg = `📦 **${catalog.length} skills available** (${installed.length} installed)\n\n`
          for (const s of catalog) {
            const status = installed.includes(s.name) ? "✅" : "⬜"
            msg += `${status} **${s.name}** — ${s.desc}\n`
          }
          await ctx.session.prompt({ sessionID, text: msg, delivery })
        },
      })

      // Command: install specific skill
      editor.add({
        name: "skill-manager-install",
        description: "Install skill(s). Usage: /skill-manager install [name] — omit name for all",
        execute: async ({ sessionID, prompt, delivery }) => {
          const target = prompt.replace("/skill-manager install", "").trim()
          try {
            await getCatalog() // ensure cache exists
            if (target) {
              // Install single skill
              const exists = execSync(`ls -d ${CACHE_DIR}/skills/${target}/ 2>/dev/null`).toString().trim()
              if (!exists) {
                await ctx.session.prompt({ sessionID, text: `❌ Skill "${target}" not found. Run /skill-manager list to see all.`, delivery })
                return
              }
              execSync(`cp -r ${CACHE_DIR}/skills/${target} ${SKILLS_DIR}/${target}`, { stdio: "ignore" })
              await ctx.session.prompt({ sessionID, text: `✅ Installed **${target}**`, delivery })
            } else {
              // Install all
              execSync(`cp -r ${CACHE_DIR}/skills/* ${SKILLS_DIR}/`, { stdio: "ignore" })
              const count = getInstalled().length
              await ctx.session.prompt({ sessionID, text: `✅ ${count} skills installed!`, delivery })
            }
          } catch (e) {
            await ctx.session.prompt({ sessionID, text: `❌ Install failed: ${e}`, delivery })
          }
        },
      })

      // Command: uninstall specific skill
      editor.add({
        name: "skill-manager-uninstall",
        description: "Remove a skill. Usage: /skill-manager uninstall <name>",
        execute: async ({ sessionID, prompt, delivery }) => {
          const target = prompt.replace("/skill-manager uninstall", "").trim()
          if (!target) {
            await ctx.session.prompt({ sessionID, text: "Usage: /skill-manager uninstall <name>", delivery })
            return
          }
          try {
            execSync(`rm -rf ${SKILLS_DIR}/${target}`, { stdio: "ignore" })
            await ctx.session.prompt({ sessionID, text: `🗑️ Removed **${target}**`, delivery })
          } catch (e) {
            await ctx.session.prompt({ sessionID, text: `❌ Uninstall failed: ${e}`, delivery })
          }
        },
      })

      // Command: search skills
      editor.add({
        name: "skill-manager-search",
        description: "Search skills by keyword. Usage: /skill-manager search <term>",
        execute: async ({ sessionID, prompt, delivery }) => {
          const term = prompt.replace("/skill-manager search", "").trim().toLowerCase()
          if (!term) {
            await ctx.session.prompt({ sessionID, text: "Usage: /skill-manager search <term>", delivery })
            return
          }
          const catalog = await getCatalog()
          const results = catalog.filter(s => s.name.toLowerCase().includes(term) || s.desc.toLowerCase().includes(term))
          if (results.length === 0) {
            await ctx.session.prompt({ sessionID, text: `🔍 No skills found for "${term}".`, delivery })
            return
          }
          let msg = `🔍 **${results.length} results** for "${term}":\n\n`
          for (const s of results) {
            msg += `**${s.name}** — ${s.desc}\n`
          }
          await ctx.session.prompt({ sessionID, text: msg, delivery })
        },
      })

      // Command: update skills
      editor.add({
        name: "skill-manager-update",
        description: "Update skills from GitHub. Usage: /skill-manager update [name] — omit name for all",
        execute: async ({ sessionID, prompt, delivery }) => {
          const target = prompt.replace("/skill-manager update", "").trim()
          try {
            execSync(`cd ${CACHE_DIR} && git pull --ff-only 2>/dev/null`, { stdio: "ignore" })
            if (target) {
              execSync(`cp -rf ${CACHE_DIR}/skills/${target} ${SKILLS_DIR}/${target}`, { stdio: "ignore" })
              await ctx.session.prompt({ sessionID, text: `✅ Updated **${target}**`, delivery })
            } else {
              execSync(`cp -rf ${CACHE_DIR}/skills/* ${SKILLS_DIR}/`, { stdio: "ignore" })
              await ctx.session.prompt({ sessionID, text: "✅ All skills updated!", delivery })
            }
          } catch (e) {
            await ctx.session.prompt({ sessionID, text: `❌ Update failed: ${e}`, delivery })
          }
        },
      })

      // Command: categories
      editor.add({
        name: "skill-manager-cats",
        description: "Show skills grouped by category",
        execute: async ({ sessionID, delivery }) => {
          const catalog = await getCatalog()
          const categories = {
            "🎨 Design & UI": ["py-side6-gui-design", "modern-web-design", "skill-creator"],
            "📄 Documentation": ["readme-generator", "technical-documentation-with-claude", "changelog-generator"],
            "🎬 Animation": ["animate", "motion-framer", "gsap-scrolltrigger", "react-spring-physics", "animejs", "lottie-animations", "review-animations", "improve-animations", "animation-vocabulary", "find-animation-opportunities"],
            "🎯 3D & WebGL": ["threejs-webgl", "react-three-fiber", "babylonjs-engine", "playcanvas-engine", "aframe-webxr", "lightweight-3d-effects", "pixijs-2d", "blender-web-pipeline", "spline-interactive", "rive-interactive", "substance-3d-texturing"],
            "📜 Scroll": ["barba-js", "locomotive-scroll", "scroll-reveal-libraries"],
            "🧩 Components": ["animated-component-libraries", "web3d-integration-patterns"],
          }
          let msg = ""
          for (const [cat, skills] of Object.entries(categories)) {
            msg += `\n### ${cat}\n`
            for (const s of skills) {
              const found = catalog.find(c => c.name === s)
              msg += `- **${s}**${found ? ` — ${found.desc}` : ""}\n`
            }
          }
          await ctx.session.prompt({ sessionID, text: msg, delivery })
        },
      })
    })

    // Auto-check on startup
    try {
      const { existsSync } = await import("node:fs")
      if (!existsSync(SKILLS_DIR) || (await ctx.storage.get("skill-manager:installed")) === null) {
        // Silently check — user can run /skill-manager install
      }
    } catch {}
  },
}
