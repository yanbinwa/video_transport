try:
    from moviepy.editor import VideoFileClip, AudioFileClip
    print("MoviePy 导入成功！")
except Exception as e:
    print(f"导入错误: {str(e)}")
    print(f"错误类型: {type(e)}")
    import sys
    print(f"Python 路径: {sys.path}")