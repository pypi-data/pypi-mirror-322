from pathlib import Path

from datasets import DatasetDict, interleave_datasets, load_dataset

main_path = Path(__file__).parent
data_path = main_path / "__data__"

configs = {"classes": 5, "train_samples": 1001, "val_ratio": 0.2, "test_samples": 1001}


def make_dataset():
    # Data pipeline
    MNIST = load_dataset("mnist", keep_in_memory=True)
    digit_ds = []
    for i in range(configs["classes"]):
        digit_ds.append(
            MNIST.filter(
                lambda example: example["label"] == i, keep_in_memory=True, num_proc=8
            )
        )
    ordered_MNIST = DatasetDict()
    # Order the digits in the dataset and select only a subset of the data
    for split in ["train", "test"]:
        ordered_MNIST[split] = interleave_datasets(
            [ds[split] for ds in digit_ds], split=split
        ).select(range(configs[f"{split}_samples"]))
    _tmp_ds = ordered_MNIST["train"].train_test_split(
        test_size=configs["val_ratio"], shuffle=False
    )
    ordered_MNIST["train"] = _tmp_ds["train"]
    ordered_MNIST["validation"] = _tmp_ds["test"]
    ordered_MNIST.set_format(type="torch", columns=["image", "label"])
    ordered_MNIST = ordered_MNIST.map(
        lambda example: {"image": example["image"] / 255.0, "label": example["label"]},
        batched=True,
        keep_in_memory=True,
        num_proc=2,
    )
    ordered_MNIST.save_to_disk(data_path)


def main():
    # Check if data_path exists, if not preprocess the data
    if not data_path.exists():
        print("Data directory not found, preprocessing data.")
        make_dataset()
    else:
        print("Data already preprocessed.")


if __name__ == "__main__":
    main()
