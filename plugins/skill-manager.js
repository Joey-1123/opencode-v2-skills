// opencode-v2-skills skill-manager — auto-manages skills from GitHub repo
// Install: copy to ~/.config/opencode/plugins/skill-manager.js
// Commands: /skill-manager install, /skill-manager update, /skill-manager list
export default {
  id: "skill-manager",
  async setup(ctx) {
    const SKILLS_REPO = "https://github.com/Joey-1123/opencode-v2-skills.git"
    const SKILLS_DIR = process.env.HOME + "/.config/opencode/skills"
    const execSync = (await import("child_process")).execSync

    // Command: install
    await ctx.command.transform((editor) => {
      editor.add({
        name: "skill-manager-install",
        description: "Install all skills from opencode-v2-skills repo",
        execute: async ({ sessionID, delivery }) => {
          try {
            execSync(`git clone --depth 1 ${SKILLS_REPO} /tmp/skills-tmp`, { stdio: "ignore" })
            execSync(`cp -r /tmp/skills-tmp/skills/* ${SKILLS_DIR}/`, { stdio: "ignore" })
            execSync(`rm -rf /tmp/skills-tmp`, { stdio: "ignore" })
            await ctx.storage.set("skill-manager:installed", new Date().toISOString())
            const count = execSync(`ls -d ${SKILLS_DIR}/*/ 2>/dev/null | wc -l`).toString().trim()
            await ctx.session.prompt({ sessionID, text: `✅ ${count} skills installed!`, delivery })
          } catch (e) {
            await ctx.session.prompt({ sessionID, text: `❌ Install failed: ${e}`, delivery })
          }
        },
      })

      // Command: update
      editor.add({
        name: "skill-manager-update",
        description: "Pull latest skills from GitHub",
        execute: async ({ sessionID, delivery }) => {
          try {
            execSync(`cd ${SKILLS_DIR}/.. && git pull --ff-only 2>/dev/null || (rm -rf skills && git clone --depth 1 ${SKILLS_REPO} skills)`, { stdio: "ignore" })
            await ctx.session.prompt({ sessionID, text: "✅ Skills updated!", delivery })
          } catch (e) {
            await ctx.session.prompt({ sessionID, text: `❌ Update failed: ${e}`, delivery })
          }
        },
      })

      // Command: list
      editor.add({
        name: "skill-manager-list",
        description: "Show installed skills count",
        execute: async ({ sessionID, delivery }) => {
          try {
            const count = execSync(`ls -d ${SKILLS_DIR}/*/ 2>/dev/null | wc -l`).toString().trim()
            await ctx.session.prompt({ sessionID, text: `📦 ${count} skills installed. Run /skill-manager install if 0.`, delivery })
          } catch {
            await ctx.session.prompt({ sessionID, text: "No skills installed. Run /skill-manager install.", delivery })
          }
        },
      })
    })

    // Auto-check on startup
    try {
      const { existsSync } = await import("node:fs")
      if (!existsSync(SKILLS_DIR) || (await ctx.storage.get("skill-manager:installed")) === null) {
        // Silently check, prompt user if needed
      }
    } catch {}
  },
}
