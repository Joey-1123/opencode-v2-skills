// opencode-v2-skills marketplace — uses npx/curl for skill management
// Commands: list, install, search, uninstall, update, categories
export default {
  id: "skill-manager",
  async setup(ctx) {
    await ctx.command.transform((editor) => {
      // list
      editor.add({
        name: "skill-manager-list",
        description: "Browse all skills in the marketplace",
        execute: async ({ sessionID, delivery }) => {
          try {
            const result = await run("list");
            await ctx.session.prompt({ sessionID, text: result, delivery });
          } catch (e) { await ctx.session.prompt({ sessionID, text: "❌ " + e, delivery }); }
        },
      });

      // install
      editor.add({
        name: "skill-manager-install",
        description: "Install skill(s). Usage: /skill-manager install [name]",
        execute: async ({ sessionID, prompt, delivery }) => {
          const name = prompt.replace("/skill-manager install", "").trim();
          try {
            const result = await run("install", name);
            await ctx.session.prompt({ sessionID, text: result, delivery });
          } catch (e) { await ctx.session.prompt({ sessionID, text: "❌ " + e, delivery }); }
        },
      });

      // uninstall
      editor.add({
        name: "skill-manager-uninstall",
        description: "Remove a skill. Usage: /skill-manager uninstall <name>",
        execute: async ({ sessionID, prompt, delivery }) => {
          const name = prompt.replace("/skill-manager uninstall", "").trim();
          if (!name) { await ctx.session.prompt({ sessionID, text: "Usage: /skill-manager uninstall <name>", delivery }); return; }
          try {
            const result = await run("uninstall", name);
            await ctx.session.prompt({ sessionID, text: result, delivery });
          } catch (e) { await ctx.session.prompt({ sessionID, text: "❌ " + e, delivery }); }
        },
      });

      // search
      editor.add({
        name: "skill-manager-search",
        description: "Search skills. Usage: /skill-manager search <term>",
        execute: async ({ sessionID, prompt, delivery }) => {
          const term = prompt.replace("/skill-manager search", "").trim();
          if (!term) { await ctx.session.prompt({ sessionID, text: "Usage: /skill-manager search <term>", delivery }); return; }
          try {
            const result = await run("search", term);
            await ctx.session.prompt({ sessionID, text: result, delivery });
          } catch (e) { await ctx.session.prompt({ sessionID, text: "❌ " + e, delivery }); }
        },
      });

      // update
      editor.add({
        name: "skill-manager-update",
        description: "Update skills. Usage: /skill-manager update [name]",
        execute: async ({ sessionID, prompt, delivery }) => {
          const name = prompt.replace("/skill-manager update", "").trim();
          try {
            const result = await run("update", name);
            await ctx.session.prompt({ sessionID, text: result, delivery });
          } catch (e) { await ctx.session.prompt({ sessionID, text: "❌ " + e, delivery }); }
        },
      });

      // categories
      editor.add({
        name: "skill-manager-categories",
        description: "Show skills grouped by category",
        execute: async ({ sessionID, delivery }) => {
          try {
            const result = await run("categories");
            await ctx.session.prompt({ sessionID, text: result, delivery });
          } catch (e) { await ctx.session.prompt({ sessionID, text: "❌ " + e, delivery }); }
        },
      });
    });

    // Auto-check on startup
    try {
      const { existsSync } = await import("node:fs");
      if (!existsSync(process.env.HOME + "/.config/opencode/skills")) {
        await ctx.session.prompt({ sessionID: null, text: "🔧 Skills not installed. Run /skill-manager install." });
      }
    } catch {}
  },
};

// Run the npx CLI
async function run(cmd, arg) {
  const { execSync } = await import("child_process");
  const args = arg ? ` "${arg}"` : "";
  const script = `npx @Joey-1123/opencode-v2-skills ${cmd}${args}`;
  try {
    const result = execSync(script, { encoding: "utf-8", timeout: 30000, stdio: ["pipe", "pipe", "pipe"] });
    return result.trim();
  } catch (e) {
    // If npx not found, try local node
    const local = `node /home/joey/projects/opencode-v2-skills/npm-package/bin/cli.js ${cmd}${args}`;
    try {
      const result = execSync(local, { encoding: "utf-8", timeout: 30000, stdio: ["pipe", "pipe", "pipe"] });
      return result.trim();
    } catch (e2) {
      return e2.stdout?.trim() || e2.stderr?.trim() || e.message;
    }
  }
}
