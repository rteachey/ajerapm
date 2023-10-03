# Better Ajera interaction portal
[Ajera](https://ajera.com/) is a project database used by our company, [KBJW Group](https://kbjwgroup.com/).

## Who are we, who am I

We're a regional civil engineering company in the midwest/atlantic/southeast. I am just a project engineer (civil) at KBJW. I mainly do calculations and project management. I do not code for a living, but I do like it. I got tasked with this because it became known I sort of know how to do this type of thing.

## Motivation:
Right now, once a week using the default Ajera GUI, PMs have to:
1. Search a project number
2. Click a project phase
3. Click a tab and then a field
4. Enter the "percent complete" for that job
5. Repeat for between half a dozen(?) and dozens of jobs (depending on the PM, it can take hours)

## Goal
Make this better!

- Something like an Excel (ie tabular/spreadsheet) GUI for PMs.
- All of their projects and phases are listed, along with (read only) info from some other useful fields, and they can enter all their % completes in a column, quickly.
- Right now: only changes to a handful of fields will be synced to the remote! Not necessary to do all fields. BUT: suppose this could change in the future when people fall in love with this awesome tool (sigh).

### Constraints
- Something like ~30 PMs updating a thousand(?) active phases a week
- Database is relatively small: something like 25k total projects right now, with an average of a handful of phases each (but some have many more)
- Greatly prefer to stick with Ajera, but might be open to a major change if there is a clear win
- If sticking with Ajera, then have to use the [Ajera API](https://help.deltek.com/Product/Ajera/api/) (a pretty simple API for read/write to database); cannot connect to database via SQL as far as I am aware, though I suppose we might be able to *host our own Ajera database (this sounds like a nightmare to me, and to IT, though)*
- Ease of use for PMs (probably means using Excel...?)
- Minimal maintenance (we're not going to hire a developer to maintain and continue developing internally)
- Little bit worried about speed right now
-- API limits to 1999 projects per request, and...
-- so far any large API requests to the remote seem pretty slow but maybe it can be better. For this reason have thought about working with a copy directly, instead of the remote, and only updating ***certain fields*** of the remote weekly.
- Keep solution simple so:
-- yours truly is actually capable of writing the thing :/
-- use familiar, widespread technology
-- we can, if needed, at some point hand off to someone familiar with the technology being used (might be willing to outsource it to a consulting developer for occasional fixes, updates, later)

### Ideas
- **Very python:** Cloud based (Azure?) python script that periodically (daily?) downloads changes to the database... to a copy somewhere? (...or maybe we don't even need a copy?); then using the copy (or just the remote?) a (dumb) Excel workbook is created for each PM that has only their projects in it. They enter new weekly info, save. Then a script is run to use those workbooks to update the copy, and then a script runs to update the remote database
-- upsides: python!
-- downsides: very custom? running afoul of "use familiar, widespread technology"?
- **Microsofty:** a ***single*** Excel sheet with a Power Query script that pulls down a table using the API; each PM can simultaneously [use a custom view](https://www.youtube.com/watch?v=aysKo3a_gHo&t=96s) while looking at the same file as everyone else, and update their phases. Then a script runs to update the remote with the new info in the .
-- upsides: **A.** seems like business development type people are probably a lot more comfortable/likely to be familiar with MS Power Query...? Maybe? **B.** no python: no environments, no 3rd party versioning to worry about, don't have to ever worry about hiring an expensive developer to fix out problems
-- downsides: no python :( 
- Ditch Ajera! (unlikely unless very very compelling)
