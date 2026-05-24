# ML — mission control for `learn-ml-nn-ai`

This repo is the **superset**: the umbrella over everything in the ML / NN / AI journey.
It holds no ML code. Its job is to **know the whole picture and steer**.

The work lives in dedicated **child repos** (gitignored here, each tracked in its own repo):
see [`meta/registry.md`](meta/registry.md).

## How to read this hub

- **The map** → [`meta/`](meta/) — what each child repo is and how it fits.
- **The compass** → [`decisions/`](decisions/) — why the journey is shaped this way.
- **The next step** → [`operational/`](operational/) — runbooks + the snapshot tool.
- **Where things stand** → [`STATUS.md`](STATUS.md) — generated; run `just snapshot` to refresh.
- **Cross-repo work** → GitHub Project (link added in Task 12).

## Refresh status

```bash
just snapshot   # reads every child repo, regenerates STATUS.md
```
