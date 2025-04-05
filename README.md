## Structure
### /src
- SvelteKit app

### /static
- /models – 3D model and AI models
- wasm files
- manifest

### /3D
- Blender file for 3D model

### /python_recognition
- Python scripts for hand gesture recognition
- Dataset (~7k images)
- Note: TFDF needs linux, use Keras 2

## Developing

```bash
npm install
npm run dev
```

## Building

To create a production version of your app:

```bash
npm run build
```

You can preview the production build with `npm run preview`.

## Docker

```bash
docker build -t pupa .
docker run -p 3000:3000 pupa
```