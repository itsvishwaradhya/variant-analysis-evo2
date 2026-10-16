import os
import sys

import modal

from fastapi import Header, HTTPException, Request
from pydantic import BaseModel, model_validator
from typing import Literal, Optional


def verify_jwt_token(authorization: str | None) -> dict:
    import jwt

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Sign in required")
    token = authorization.removeprefix("Bearer ").strip()
    secret = os.environ.get("JWT_SECRET")
    if not secret:
        raise HTTPException(status_code=500, detail="Server auth not configured")
    try:
        return jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Session expired, sign in again")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid session")


MAX_DELETION_LENGTH = 500
MAX_INSERTION_LENGTH = 500

# Pathogenicity thresholds below were calibrated on BRCA1 SNVs
# (run_brca1_analysis). They are reused provisionally for indels until an
# indel-specific calibration exists; responses flag provisional=True.
SNV_THRESHOLD = -0.0009178519
SNV_LOF_STD = 0.0015140239
SNV_FUNC_STD = 0.0009016589

VARIANT_THRESHOLDS = {
    "snv": {"threshold": SNV_THRESHOLD, "lof_std": SNV_LOF_STD,
            "func_std": SNV_FUNC_STD, "provisional": False},
    "deletion": {"threshold": SNV_THRESHOLD, "lof_std": SNV_LOF_STD,
                 "func_std": SNV_FUNC_STD, "provisional": True},
    "insertion": {"threshold": SNV_THRESHOLD, "lof_std": SNV_LOF_STD,
                  "func_std": SNV_FUNC_STD, "provisional": True},
    "delins": {"threshold": SNV_THRESHOLD, "lof_std": SNV_LOF_STD,
               "func_std": SNV_FUNC_STD, "provisional": True},
}


def _validate_inserted_sequence(value, field_name="inserted_sequence"):
    if value is None:
        raise ValueError(f"{field_name} is required")
    seq = str(value).upper().replace(" ", "").replace("\n", "")
    if not seq:
        raise ValueError(f"{field_name} must not be empty")
    if len(seq) > MAX_INSERTION_LENGTH:
        raise ValueError(
            f"{field_name} must be at most {MAX_INSERTION_LENGTH}bp")
    if any(b not in ("A", "T", "C", "G") for b in seq):
        raise ValueError(f"{field_name} must contain only A, T, C, G")
    return seq


class VariantRequest(BaseModel):
    variant_position: int
    variant_type: Literal["snv", "deletion", "insertion", "delins"] = "snv"
    alternative: Optional[str] = None
    deletion_length: Optional[int] = None
    inserted_sequence: Optional[str] = None
    genome: str
    chromosome: str

    @model_validator(mode="after")
    def validate_variant(self):
        if self.variant_type == "snv":
            if self.alternative is None:
                raise ValueError("alternative is required for SNV")
            alt = self.alternative.upper()
            if alt not in ("A", "T", "C", "G"):
                raise ValueError("SNV alternative must be one of A, T, C, G")
            self.alternative = alt
            if self.deletion_length is not None:
                raise ValueError("deletion_length must not be set for SNV")
            if self.inserted_sequence not in (None, ""):
                raise ValueError("inserted_sequence must not be set for SNV")
            self.inserted_sequence = None
        elif self.variant_type == "deletion":
            if self.alternative not in (None, "", "-"):
                raise ValueError(
                    "alternative must not be set for deletion (use deletion_length)")
            self.alternative = None
            if self.deletion_length is None:
                raise ValueError("deletion_length is required for deletion")
            if not isinstance(self.deletion_length, int):
                raise ValueError("deletion_length must be an integer")
            if self.deletion_length < 1 or self.deletion_length > MAX_DELETION_LENGTH:
                raise ValueError(
                    f"deletion_length must be between 1 and {MAX_DELETION_LENGTH}")
            if self.inserted_sequence not in (None, ""):
                raise ValueError(
                    "inserted_sequence must not be set for deletion (use delins)")
            self.inserted_sequence = None
        elif self.variant_type == "insertion":
            if self.alternative not in (None, "", "-"):
                raise ValueError(
                    "alternative must not be set for insertion (use inserted_sequence)")
            self.alternative = None
            if self.deletion_length is not None:
                raise ValueError(
                    "deletion_length must not be set for insertion (use delins)")
            self.inserted_sequence = _validate_inserted_sequence(
                self.inserted_sequence)
        elif self.variant_type == "delins":
            if self.alternative not in (None, "", "-"):
                raise ValueError(
                    "alternative must not be set for delins "
                    "(use deletion_length + inserted_sequence)")
            self.alternative = None
            if self.deletion_length is None:
                raise ValueError("deletion_length is required for delins")
            if not isinstance(self.deletion_length, int):
                raise ValueError("deletion_length must be an integer")
            if self.deletion_length < 1 or self.deletion_length > MAX_DELETION_LENGTH:
                raise ValueError(
                    f"deletion_length must be between 1 and {MAX_DELETION_LENGTH}")
            self.inserted_sequence = _validate_inserted_sequence(
                self.inserted_sequence)
        return self

evo2_image = (
    modal.Image.from_registry(
        "nvidia/cuda:12.6.3-devel-ubuntu22.04",
        add_python="3.12",
    )
    .apt_install(
        "build-essential",
        "cmake",
        "ninja-build",
        "git",
        "gcc",
        "g++",
    )
    .env({
        "CC": "/usr/bin/gcc",
        "CXX": "/usr/bin/g++",
        "CUDA_HOME": "/usr/local/cuda",
    })
    .pip_install(
        "packaging",
        "psutil",
        "ninja",
        "setuptools",
        "wheel",
        "huggingface_hub"
    )
    .pip_install(
        "torch==2.7.1",
        index_url="https://download.pytorch.org/whl/cu126",
    )
    .pip_install(
        "flash-attn==2.8.0.post2",
        extra_options="--no-build-isolation",
    )
    .run_commands(
        "git clone --recurse-submodules "
        "https://github.com/ArcInstitute/evo2.git /evo2"
    )
    .run_commands(
        "cd /evo2 && pip install ."
    )
    .pip_install_from_requirements("requirements.txt")
)

# evo2_image = (
#     modal.Image.from_registry(
#         "nvidia/cuda:12.4.0-devel-ubuntu22.04", add_python="3.12"
#     )
#     .apt_install(
#         ["build-essential", "cmake", "ninja-build",
#             "libcudnn8", "libcudnn8-dev", "git", "gcc", "g++"]
#     )
#     .env({
#         "CC": "/usr/bin/gcc",
#         "CXX": "/usr/bin/g++",
#     })
#     .run_commands("git clone --recurse-submodules https://github.com/ArcInstitute/evo2.git && cd evo2 && pip install .")
#     .run_commands("pip uninstall -y transformer-engine transformer_engine")
#     .run_commands("pip install 'transformer_engine[pytorch]==1.13' --no-build-isolation")
#     .pip_install_from_requirements("requirements.txt")
# ) 

app = modal.App("variant-analysis-evo2", image=evo2_image)

volume = modal.Volume.from_name("hf_cache", create_if_missing=True)
mount_path = "/root/.cache/huggingface"


@app.function(gpu="H100", volumes={mount_path: volume}, timeout=1000)
def run_brca1_analysis():
    import base64
    from io import BytesIO
    from Bio import SeqIO
    import gzip
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import os
    import seaborn as sns
    from sklearn.metrics import roc_auc_score, roc_curve

    from evo2 import Evo2

    WINDOW_SIZE = 8192

    print("Loading evo2 model...")
    model = Evo2('evo2_7b')
    print("Evo2 model loaded")

    brca1_df = pd.read_excel(
        '/evo2/notebooks/brca1/41586_2018_461_MOESM3_ESM.xlsx',
        header=2,
    )
    brca1_df = brca1_df[[
        'chromosome', 'position (hg19)', 'reference', 'alt', 'function.score.mean', 'func.class',
    ]]

    brca1_df.rename(columns={
        'chromosome': 'chrom',
        'position (hg19)': 'pos',
        'reference': 'ref',
        'alt': 'alt',
        'function.score.mean': 'score',
        'func.class': 'class',
    }, inplace=True)

    # Convert to two-class system
    brca1_df['class'] = brca1_df['class'].replace(['FUNC', 'INT'], 'FUNC/INT')

    with gzip.open('/evo2/notebooks/brca1/GRCh37.p13_chr17.fna.gz', "rt") as handle:
        for record in SeqIO.parse(handle, "fasta"):
            seq_chr17 = str(record.seq)
            break

    # Build mappings of unique reference sequences
    ref_seqs = []
    ref_seq_to_index = {}

    # Parse sequences and store indexes
    ref_seq_indexes = []
    var_seqs = []

    brca1_subset = brca1_df.iloc[:500].copy()

    for _, row in brca1_subset.iterrows():
        p = row["pos"] - 1  # Convert to 0-indexed position
        full_seq = seq_chr17

        ref_seq_start = max(0, p - WINDOW_SIZE//2)
        ref_seq_end = min(len(full_seq), p + WINDOW_SIZE//2)
        ref_seq = seq_chr17[ref_seq_start:ref_seq_end]
        snv_pos_in_ref = min(WINDOW_SIZE//2, p)
        var_seq = ref_seq[:snv_pos_in_ref] + \
            row["alt"] + ref_seq[snv_pos_in_ref+1:]

        # Get or create index for reference sequence
        if ref_seq not in ref_seq_to_index:
            ref_seq_to_index[ref_seq] = len(ref_seqs)
            ref_seqs.append(ref_seq)

        ref_seq_indexes.append(ref_seq_to_index[ref_seq])
        var_seqs.append(var_seq)

    ref_seq_indexes = np.array(ref_seq_indexes)

    print(
        f'Scoring likelihoods of {len(ref_seqs)} reference sequences with Evo 2...')
    ref_scores = model.score_sequences(ref_seqs)

    print(
        f'Scoring likelihoods of {len(var_seqs)} variant sequences with Evo 2...')
    var_scores = model.score_sequences(var_seqs)

    # Subtract score of corresponding reference sequences from scores of variant sequences
    delta_scores = np.array(var_scores) - np.array(ref_scores)[ref_seq_indexes]

    # Add delta scores to dataframe
    brca1_subset[f'evo2_delta_score'] = delta_scores

    y_true = (brca1_subset['class'] == 'LOF')
    auroc = roc_auc_score(y_true, -brca1_subset['evo2_delta_score'])

    # --- Calculate threshold START
    y_true = (brca1_subset["class"] == "LOF")

    fpr, tpr, thresholds = roc_curve(y_true, -brca1_subset["evo2_delta_score"])

    optimal_idx = (tpr - fpr).argmax()

    optimal_threshold = -thresholds[optimal_idx]

    lof_scores = brca1_subset.loc[brca1_subset["class"]
                                  == "LOF", "evo2_delta_score"]
    func_scores = brca1_subset.loc[brca1_subset["class"]
                                   == "FUNC/INT", "evo2_delta_score"]

    lof_std = lof_scores.std()
    func_std = func_scores.std()

    confidence_params = {
        "threshold": optimal_threshold,
        "lof_std": lof_std,
        "func_std": func_std
    }

    print("Confidence params:", confidence_params)

    # --- Calculate threshold END

    plt.figure(figsize=(4, 2))

    # Plot stripplot of distributions
    p = sns.stripplot(
        data=brca1_subset,
        x='evo2_delta_score',
        y='class',
        hue='class',
        order=['FUNC/INT', 'LOF'],
        palette=['#777777', 'C3'],
        size=2,
        jitter=0.3,
    )

    # Mark medians from each distribution
    sns.boxplot(showmeans=True,
                meanline=True,
                meanprops={'visible': False},
                medianprops={'color': 'k', 'ls': '-', 'lw': 2},
                whiskerprops={'visible': False},
                zorder=10,
                x="evo2_delta_score",
                y="class",
                data=brca1_subset,
                showfliers=False,
                showbox=False,
                showcaps=False,
                ax=p)
    plt.xlabel('Delta likelihood score, Evo 2')
    plt.ylabel('BRCA1 SNV class')
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return {'variants': brca1_subset.to_dict(orient="records"), "plot": plot_data, "auroc": auroc}


@app.function()
def brca1_example():
    import base64
    from io import BytesIO
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg

    print("Running BRCA1 variant analysis with Evo2...")

    # Run inference
    result = run_brca1_analysis.remote()

    if "plot" in result:
        plot_data = base64.b64decode(result["plot"])
        with open("brca1_analysis_plot.png", "wb") as f:
            f.write(plot_data)

        img = mpimg.imread(BytesIO(plot_data))
        plt.figure(figsize=(10, 5))
        plt.imshow(img)
        plt.axis("off")
        plt.show()


def get_genome_sequence(position, genome: str, chromosome: str, window_size=8192):
    import requests

    half_window = window_size // 2
    start = max(0, position - 1 - half_window)
    end = position - 1 + half_window + 1

    print(
        f"Fetching {window_size}bp window around position {position} from UCSC API..")
    print(f"Coordinates: {chromosome}:{start}-{end} ({genome})")

    api_url = f"https://api.genome.ucsc.edu/getData/sequence?genome={genome};chrom={chromosome};start={start};end={end}"
    response = requests.get(api_url)

    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch genome sequence from UCSC API: {response.status_code}")

    genome_data = response.json()

    if "dna" not in genome_data:
        error = genome_data.get("error", "Unknown error")
        raise Exception(f"UCSC API errpr: {error}")

    sequence = genome_data.get("dna", "").upper()
    expected_length = end - start
    if len(sequence) != expected_length:
        print(
            f"Warning: received sequence length ({len(sequence)}) differs from expected ({expected_length})")

    print(
        f"Loaded reference genome sequence window (length: {len(sequence)} bases)")

    return sequence, start


def analyze_variant(relative_pos_in_window, reference, alternative, window_seq, model,
                     variant_type: str = "snv", deletion_length: int | None = None,
                     inserted_sequence: str | None = None):
    if variant_type == "deletion":
        n = deletion_length or 1
        # Delete the reference nucleotide(s): variation sequence is one
        # (or n) bases shorter. Scoring logic below is unchanged.
        var_seq = window_seq[:relative_pos_in_window] + \
            window_seq[relative_pos_in_window+n:]
        alternative_out = "-"
    elif variant_type == "insertion":
        ins = (inserted_sequence or "").upper()
        # Insert after the anchor base at relative_pos.
        var_seq = window_seq[:relative_pos_in_window+1] + ins + \
            window_seq[relative_pos_in_window+1:]
        alternative_out = f"ins{ins}"
    elif variant_type == "delins":
        n = deletion_length or 1
        ins = (inserted_sequence or "").upper()
        var_seq = window_seq[:relative_pos_in_window] + ins + \
            window_seq[relative_pos_in_window+n:]
        alternative_out = ins
    else:
        var_seq = window_seq[:relative_pos_in_window] + \
            alternative + window_seq[relative_pos_in_window+1:]
        alternative_out = alternative

    ref_score = model.score_sequences([window_seq])[0]
    var_score = model.score_sequences([var_seq])[0]

    delta_score = var_score - ref_score

    params = VARIANT_THRESHOLDS.get(variant_type, VARIANT_THRESHOLDS["snv"])
    threshold = params["threshold"]
    lof_std = params["lof_std"]
    func_std = params["func_std"]

    if delta_score < threshold:
        prediction = "Likely pathogenic"
        confidence = min(1.0, abs(delta_score - threshold) / lof_std)
    else:
        prediction = "Likely benign"
        confidence = min(1.0, abs(delta_score - threshold) / func_std)

    result = {
        "reference": reference,
        "alternative": alternative_out,
        "variant_type": variant_type,
        "delta_score": float(delta_score),
        "prediction": prediction,
        "classification_confidence": float(confidence),
        "threshold_used": float(threshold),
        "provisional_prediction": bool(params["provisional"]),
    }
    if variant_type in ("deletion", "delins"):
        result["deletion_length"] = int(deletion_length or 1)
    if variant_type in ("insertion", "delins"):
        result["inserted_sequence"] = (inserted_sequence or "").upper()
    return result


@app.cls(gpu="H100", volumes={mount_path: volume}, max_containers=3, retries=2, scaledown_window=120, secrets=[modal.Secret.from_name("auth-secret")])
class Evo2Model:
    @modal.enter()
    def load_evo2_model(self):
        from evo2 import Evo2
        print("Loading evo2 model...")
        self.model = Evo2('evo2_7b')
        print("Evo2 model loaded")

    def _verify_jwt(self, authorization: str | None) -> dict:
        import jwt

        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Sign in required")
        token = authorization.removeprefix("Bearer ").strip()
        secret = os.environ.get("JWT_SECRET")
        if not secret:
            raise HTTPException(status_code=500, detail="Server auth not configured")
        try:
            return jwt.decode(token, secret, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Session expired, sign in again")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid session")

    # @modal.method()
    @modal.fastapi_endpoint(method="POST")
    def analyze_single_variant(self, request: VariantRequest, req: Request):
        self._verify_jwt(req.headers.get("authorization"))
        variant_position = request.variant_position
        variant_type = request.variant_type or "snv"
        alternative = request.alternative
        deletion_length = request.deletion_length
        inserted_sequence = request.inserted_sequence
        genome = request.genome
        chromosome = request.chromosome

        print("Genome:", genome)
        print("Chromosome:", chromosome)
        print("Variant position:", variant_position)
        print("Variant type:", variant_type)
        print("Variant alternative:", alternative)
        print("Deletion length:", deletion_length)
        print("Inserted sequence:", inserted_sequence)

        WINDOW_SIZE = 8192

        # Center the context window on the variant midpoint so multi-base
        # deletions/delins keep balanced flanking sequence on both sides.
        if variant_type in ("deletion", "delins") and deletion_length:
            fetch_center = variant_position + (deletion_length - 1) // 2
        else:
            fetch_center = variant_position

        window_seq, seq_start = get_genome_sequence(
            position=fetch_center,
            genome=genome,
            chromosome=chromosome,
            window_size=WINDOW_SIZE
        )

        print(f"Fetched genome seauence window, first 100: {window_seq[:100]}")

        relative_pos = variant_position - 1 - seq_start
        print(f"Relative position within window: {relative_pos}")

        if relative_pos < 0 or relative_pos >= len(window_seq):
            raise ValueError(
                f"Variant position {variant_position} is outside the fetched window (start={seq_start+1}, end={seq_start+len(window_seq)})")

        if variant_type == "deletion":
            n = deletion_length or 1
            if relative_pos + n > len(window_seq):
                raise ValueError(
                    f"Deletion of {n}bp at {variant_position} extends beyond the fetched window "
                    f"(start={seq_start+1}, end={seq_start+len(window_seq)})")
            reference = window_seq[relative_pos:relative_pos+n]
            print(f"Reference (deleted) is: {reference}")
        elif variant_type == "insertion":
            inserted_sequence = _validate_inserted_sequence(inserted_sequence)
            reference = window_seq[relative_pos]
            print(f"Insertion anchor is: {reference}, insert: {inserted_sequence}")
        elif variant_type == "delins":
            n = deletion_length or 1
            if relative_pos + n > len(window_seq):
                raise ValueError(
                    f"Delins of {n}bp at {variant_position} extends beyond the fetched window "
                    f"(start={seq_start+1}, end={seq_start+len(window_seq)})")
            inserted_sequence = _validate_inserted_sequence(inserted_sequence)
            reference = window_seq[relative_pos:relative_pos+n]
            print(f"Delins reference is: {reference}, insert: {inserted_sequence}")
        else:
            if alternative is None:
                raise ValueError("alternative is required for SNV")
            alternative = alternative.upper()
            if alternative not in ("A", "T", "C", "G"):
                raise ValueError("SNV alternative must be one of A, T, C, G")
            reference = window_seq[relative_pos]
            print("Reference is: " + reference)

        # Analyze the variant
        result = analyze_variant(
            relative_pos_in_window=relative_pos,
            reference=reference,
            alternative=alternative,
            window_seq=window_seq,
            model=self.model,
            variant_type=variant_type,
            deletion_length=deletion_length,
            inserted_sequence=inserted_sequence,
        )

        result["position"] = variant_position

        return result


@app.local_entrypoint()
def main():
    # Example of how you'd call the deployed Modal Function from your client
    import requests
    import json    # brca1_example.remote()

    evo2Model = Evo2Model()

    url = evo2Model.analyze_single_variant.get_web_url()

    payload = {
        "variant_position": 43119628,
        "variant_type": "snv",
        "alternative": "G",
        "genome": "hg38",
        "chromosome": "chr17"
    }

    headers = {
        "Content-Type": "application/json"
    }

    # Attach auth when available: endpoint requires a Bearer JWT.
    # Use EVO2_JWT/JWT_TOKEN directly, or mint a dev token from JWT_SECRET.
    # Falls back to reading ../evo2-frontend/.env so `modal run` works
    # without manually exporting the secret in every shell.
    def _load_secret_from_dotenv():
        try:
            from pathlib import Path
            candidates = [
                Path(__file__).resolve().parent.parent / "evo2-frontend" / ".env",
                Path(__file__).resolve().parent / ".env",
            ]
            for p in candidates:
                if not p.is_file():
                    continue
                for line in p.read_text().splitlines():
                    s = line.strip()
                    if not s or s.startswith("#") or "=" not in s:
                        continue
                    k, _, v = s.partition("=")
                    if k.strip() == "JWT_SECRET":
                        v = v.strip().strip('"').strip("'").strip()
                        if v:
                            print(f"Loaded JWT_SECRET from {p}")
                            return v
        except Exception as exc:
            print(f"Could not read JWT_SECRET from dotenv: {exc}")
        return None

    token = os.environ.get("EVO2_JWT") or os.environ.get("JWT_TOKEN")
    token_source = "env EVO2_JWT/JWT_TOKEN" if token else None
    if not token:
        secret = os.environ.get("JWT_SECRET")
        secret_source = "env JWT_SECRET" if secret else None
        if not secret:
            secret = _load_secret_from_dotenv()
            secret_source = "frontend .env" if secret else None
        if secret:
            try:
                import time
                import jwt as pyjwt
                now = int(time.time())
                token = pyjwt.encode(
                    {"sub": "dev", "email": "dev@localhost",
                     "iat": now, "exp": now + 3600},
                    secret,
                    algorithm="HS256",
                )
                token_source = f"minted dev JWT ({secret_source})"
            except Exception as exc:
                print(f"Could not mint dev JWT: {exc}")

    if token:
        headers["Authorization"] = f"Bearer {token}"
        print(f"Using auth token ({token_source})")
    else:
        print("Warning: no EVO2_JWT/JWT_TOKEN, JWT_SECRET env, or frontend .env found; "
              "expect 401 'Sign in required' from analyze_single_variant")

    response = requests.post(url, json=payload, headers=headers)
    print(f"Status: {response.status_code}")
    try:
        response.raise_for_status()
    except requests.HTTPError:
        # Surface the server's error body instead of a bare traceback
        print(f"Request failed ({response.status_code}): {response.text[:1000]}")
        raise
    result = response.json()
    print(result)
