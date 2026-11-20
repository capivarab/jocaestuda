#!/usr/bin/env python3
"""Joca Estuda — vídeo piloto gerado de dados estruturados do próprio site.
Lê a aula de Probabilidade no HTML; nenhuma foto do Bernoulli é publicada.
Dependências: pillow, pydub, ffmpeg, espeak, DejaVu Sans.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from pydub import AudioSegment
import argparse, json, re, subprocess, tempfile

ROOT = Path(__file__).resolve().parent
BG=(250,246,238);DARK=(62,47,34);GREEN=(74,107,77)
TERRA=(168,99,43);WHITE=(255,255,255);CREAM=(255,242,218)
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
W,H=1280,720

def font(px,bold=False):
    return ImageFont.truetype(BOLD if bold else FONT,px)

def wrap(draw,text,f,max_width):
    words=text.split()
    lines=[];buf=""
    for word in words:
        trial=(buf+" "+word).strip()
        if draw.textbbox((0,0),trial,font=f)[2] <= max_width:
            buf=trial
        else:
            if buf: lines.append(buf)
            buf=word
    if buf:lines.append(buf)
    return lines

def avatar(draw,who):
    if who=="JORUTO":
        draw.ellipse((57,330,222,495),fill=(226,178,125),outline=DARK,width=5)
        draw.polygon([(51,369),(58,296),(100,329),(133,293),(181,316),(215,296),(222,369)],fill=(55,46,43))
        draw.rounded_rectangle((67,351,211,387),radius=9,fill=(49,96,130))
        draw.ellipse((108,413,120,425),fill=DARK)
        draw.ellipse((162,413,174,425),fill=DARK)
        draw.arc((117,443,169,471),5,165,fill=DARK,width=3)
        draw.rounded_rectangle((70,495,218,615),radius=27,fill=TERRA)
    else:
        draw.ellipse((48,356,229,580),fill=(137,96,60),outline=DARK,width=4)
        draw.ellipse((64,324,111,370),fill=(137,96,60))
        draw.ellipse((173,324,220,370),fill=(137,96,60))
        draw.ellipse((103,408,120,424),fill=DARK)
        draw.ellipse((174,408,191,424),fill=DARK)
        draw.ellipse((117,448,188,490),fill=(184,140,94))
        draw.ellipse((143,453,163,465),fill=DARK)
        draw.polygon([(66,542),(135,514),(191,542),(226,631),(45,631)],fill=(225,234,222))
        draw.line((115,540,140,596,178,538),fill=GREEN,width=9)

def frame(path,who,title,text,tip,n,total):
    img=Image.new("RGB",(W,H),BG);d=ImageDraw.Draw(img)
    d.rectangle((0,0,W,111),fill=DARK)
    d.text((45,30),"JOCA ESTUDA  |  MISSÃO 2: A CHANCE NINJA",font=font(30,True),fill=WHITE)
    d.rounded_rectangle((45,137,1230,652),radius=30,fill=WHITE,outline=(143,174,140),width=5)
    d.text((75,162),title,font=font(37,True),fill=TERRA)
    avatar(d,who)
    d.text((59,634),who,font=font(21,True),fill=DARK)
    d.rounded_rectangle((258,247,1194,503),radius=22,fill=(244,247,240))
    f=font(35,False);lines=wrap(d,text,f,876)
    if len(lines)>5:
        f=font(30);lines=wrap(d,text,f,882)
    for i,line in enumerate(lines[:6]):
        d.text((282,272+i*51),line,font=f,fill=DARK)
    d.rounded_rectangle((257,528,1191,616),radius=13,fill=CREAM)
    f2=font(22,True)
    tips=wrap(d,"PENSE ASSIM: "+tip,f2,876)
    for j,line in enumerate(tips[:3]):
        d.text((275,540+j*27),line,font=f2,fill=DARK)
    d.rectangle((0,692,W,H),fill=(229,222,212))
    d.rectangle((0,692,int(W*(n+1)/total),701),fill=GREEN)
    d.text((44,702),f"CENA {n+1} DE {total}   |   PROBABILIDADE — 7º ANO",font=font(13,True),fill=DARK)
    img.save(path,optimize=True)

def cmd(args):
    subprocess.run(args,check=True)

def timestamp(seconds):
    milli=round(seconds*1000);h,milli=divmod(milli,3600000)
    m,milli=divmod(milli,60000);s,ms=divmod(milli,1000)
    return f"{h:02}:{m:02}:{s:02}.{ms:03}"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",default="piloto/video/missao2_chance_ninja.mp4")
    args=ap.parse_args()
    path=Path(args.output).resolve();path.parent.mkdir(parents=True,exist_ok=True)
    source=(ROOT/"probabilidade.html").read_text(encoding="utf-8")
    m=re.search(r'<script type="application/json" id="dados-licao">(.*?)</script>',source,re.S)
    if not m:raise RuntimeError("Dados estruturados não encontrados")
    data=json.loads(m.group(1))
    slides=[]
    for sec in data["etapas"]:
        for who,talk in sec["falas"]:
            slides.append((who,sec["titulo"],talk,sec["macete"],650))
    for n,q in enumerate(data["perguntas"],1):
        slides.append(("SENSEI",f"Pergunta {n}",q["pergunta"],"Pense antes de ouvir a resposta.",3600))
        slides.append(("JORUTO",f"Resposta {n}",q["opcoes"][q["correta"]]+". "+q["explicacao"],"Confira por que a resposta está certa.",850))
    with tempfile.TemporaryDirectory(prefix="joca_video_") as td:
        work=Path(td);audio=AudioSegment.silent(duration=0,frame_rate=44100).set_channels(2)
        entries=[];subtitle=[];cursor=0.
        for idx,(who,title,speech,tip,pause) in enumerate(slides):
            wav=work/f"fala_{idx:03}.wav";png=work/f"quadro_{idx:03}.png"
            cmd(["espeak","-v","pt-br","-s",("143" if who=="JORUTO" else "123"),"-p",("55" if who=="JORUTO" else "39"),"-w",str(wav),speech])
            part=AudioSegment.from_wav(wav).set_frame_rate(44100).set_channels(2)
            frame(png,who,title,speech,tip,idx,len(slides))
            duration=(len(part)+pause)/1000
            entries.append((png,duration))
            subtitle.append((cursor,cursor+len(part)/1000,speech))
            cursor+=duration
            audio+=part+AudioSegment.silent(duration=pause,frame_rate=44100).set_channels(2)
        wavall=work/"narracao.wav";audio.export(wavall,format="wav")
        concat=work/"frames.txt"
        with concat.open("w",encoding="utf-8") as f:
            for pic,dur in entries:
                f.write(f"file '{pic}'\n")
                f.write(f"duration {dur:.4f}\n")
            f.write(f"file '{entries[-1][0]}'\n")
        cap=path.with_suffix(".vtt")
        with cap.open("w",encoding="utf-8") as f:
            f.write("WEBVTT\n\n")
            for i,(start,end,spoken) in enumerate(subtitle,1):
                f.write(f"{i}\n{timestamp(start)} --> {timestamp(end)}\n{spoken}\n\n")
        cmd(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",str(concat),
             "-i",str(wavall),"-vf","fps=24,format=yuv420p","-c:v","libx264",
             "-profile:v","baseline","-level","3.1","-bf","0","-preset","veryfast","-crf","23",
             "-c:a","aac","-b:a","128k","-ar","44100","-ac","2",
             "-movflags","+faststart","-shortest",str(path)])
    print(f"Gerados: {path} ({path.stat().st_size/1024/1024:.1f} MiB); {len(slides)} cenas")

if __name__=="__main__":main()
