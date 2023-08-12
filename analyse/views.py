from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from Bio import SeqIO
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def analyze_fastq(request):
    if request.method == 'POST' and request.FILES['fastq_file']:
        uploaded_file = request.FILES['fastq_file']
        fs = FileSystemStorage()
        file_path = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(file_path)

        gc_content = []
        quality_scores = []
        qc_statuses = []

        quality_score_threshold = 30

        # Process the FASTQ file
        with open(file_path, 'r') as fastq_file:
            for record in SeqIO.parse(fastq_file, 'fastq'):
                sequence = record.seq
                gc_content.append((sequence.count('G') + sequence.count('C')) / len(sequence))
                avg_quality = sum(record.letter_annotations['phred_quality']) / len(sequence)
                quality_scores.append(avg_quality)

        # Create GC Content Plot
        plt.figure(figsize=(10, 4))
        plt.subplot(1, 2, 1)
        plt.hist(gc_content, bins=20, color='b', alpha=0.7)
        plt.xlabel('GC Content')
        plt.ylabel('Frequency')

        # Create Quality Scores Plot
        plt.subplot(1, 2, 2)
        plt.hist(quality_scores, bins=20, color='g', alpha=0.7)
        plt.xlabel('Average Quality Score')
        plt.ylabel('Frequency')

        # Convert plot to base64 image
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.read()).decode()

        context = {
            'file_url': file_url,
            'gc_img': img_base64,
        }

        return render(request, 'analysis_result.html', context)

    return render(request, 'analyze.html')
