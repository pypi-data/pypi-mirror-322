import numpy as np
from Moral88.utils import DataValidator
from scipy.spatial.distance import directed_hausdorff
from sklearn.metrics import f1_score as sklearn_f1_score

validator = DataValidator()

def intersection_over_union(y_true, y_pred, num_classes, library=None, flatten=True):
    """
    Computes Intersection over Union (IoU).
    """
    y_true, y_pred = validator.validate_segmentation_inputs(y_true, y_pred)
    validator.validate_classes(y_true, num_classes)
    validator.validate_classes(y_pred, num_classes)

    if flatten:
        y_true = y_true.ravel()
        y_pred = y_pred.ravel()

    if library == 'Moral88' or library is None:
        iou_per_class = []
        for cls in range(num_classes):
            intersection = np.logical_and(y_true == cls, y_pred == cls).sum()
            union = np.logical_or(y_true == cls, y_pred == cls).sum()
            iou = intersection / union if union > 0 else 0
            iou_per_class.append(iou)

        mean_iou = np.mean(iou_per_class)
        return iou_per_class, mean_iou

    elif library == 'torch':
        import torch
        y_true_tensor = torch.tensor(y_true, dtype=torch.float32)
        y_pred_tensor = torch.tensor(y_pred, dtype=torch.float32)
        iou = torch.mean((y_true_tensor * y_pred_tensor).sum(dim=1) / (y_true_tensor + y_pred_tensor - y_true_tensor * y_pred_tensor).sum(dim=1))
        return iou.item()

    elif library == 'tensorflow':
        import tensorflow as tf
        intersection = tf.reduce_sum(tf.cast(y_true == y_pred, tf.float32))
        union = tf.reduce_sum(tf.cast(y_true | y_pred, tf.float32))
        iou = intersection / union if union > 0 else 0
        return iou.numpy()

    raise ValueError("Unsupported library for IoU.")

def dice_coefficient(y_true, y_pred, num_classes, library=None, flatten=True):
    """
    Computes Dice Coefficient.
    """
    y_true, y_pred = validator.validate_segmentation_inputs(y_true, y_pred)
    validator.validate_classes(y_true, num_classes)
    validator.validate_classes(y_pred, num_classes)

    if flatten:
        y_true = y_true.ravel()
        y_pred = y_pred.ravel()

    if library == 'Moral88' or library is None:
        dice_per_class = []
        for cls in range(num_classes):
            intersection = np.logical_and(y_true == cls, y_pred == cls).sum()
            total = (y_true == cls).sum() + (y_pred == cls).sum()
            dice = (2 * intersection) / total if total > 0 else 0
            dice_per_class.append(dice)

        mean_dice = np.mean(dice_per_class)
        return dice_per_class, mean_dice

    elif library == 'torch':
        import torch
        y_true_tensor = torch.tensor(y_true, dtype=torch.float32)
        y_pred_tensor = torch.tensor(y_pred, dtype=torch.float32)
        intersection = torch.sum(y_true_tensor * y_pred_tensor)
        total = torch.sum(y_true_tensor) + torch.sum(y_pred_tensor)
        dice = (2 * intersection) / total if total > 0 else 0
        return dice.item()

    elif library == 'tensorflow':
        import tensorflow as tf
        y_true_tensor = tf.convert_to_tensor(y_true, dtype=tf.float32)
        y_pred_tensor = tf.convert_to_tensor(y_pred, dtype=tf.float32)
        intersection = tf.reduce_sum(y_true_tensor * y_pred_tensor)
        total = tf.reduce_sum(y_true_tensor) + tf.reduce_sum(y_pred_tensor)
        dice = (2 * intersection) / total if total > 0 else 0
        return dice.numpy()

    raise ValueError("Unsupported library for Dice Coefficient.")

def pixel_accuracy(y_true, y_pred, library=None):
    """
    Computes Pixel Accuracy.
    """
    y_true, y_pred = validator.validate_segmentation_inputs(y_true, y_pred)

    if library == 'Moral88' or library is None:
        correct = (y_true == y_pred).sum()
        total = y_true.size
        accuracy = correct / total
        return accuracy

    elif library == 'torch':
        import torch
        y_true_tensor = torch.tensor(y_true, dtype=torch.float32)
        y_pred_tensor = torch.tensor(y_pred, dtype=torch.float32)
        correct = torch.sum(y_true_tensor == y_pred_tensor)
        total = torch.numel(y_true_tensor)
        accuracy = correct / total
        return accuracy.item()

    elif library == 'tensorflow':
        import tensorflow as tf
        y_true_tensor = tf.convert_to_tensor(y_true, dtype=tf.float32)
        y_pred_tensor = tf.convert_to_tensor(y_pred, dtype=tf.float32)
        correct = tf.reduce_sum(tf.cast(y_true_tensor == y_pred_tensor, tf.float32))
        total = tf.size(y_true_tensor, out_type=tf.float32)
        accuracy = correct / total
        return accuracy.numpy()

    raise ValueError("Unsupported library for Pixel Accuracy.")

def hausdorff_distance(y_true, y_pred, library=None):
    """
    Computes Hausdorff Distance.
    """
    y_true, y_pred = validator.validate_segmentation_inputs(y_true, y_pred)

    if library == 'Moral88' or library is None:
        y_true_points = np.argwhere(y_true > 0)
        y_pred_points = np.argwhere(y_pred > 0)

        distance = max(directed_hausdorff(y_true_points, y_pred_points)[0],
                       directed_hausdorff(y_pred_points, y_true_points)[0])
        return distance

    raise ValueError("Unsupported library for Hausdorff Distance.")

def f1_score(y_true, y_pred, num_classes, library=None, flatten=True):
    """
    Computes F1 Score.
    """
    y_true, y_pred = validator.validate_segmentation_inputs(y_true, y_pred)
    validator.validate_classes(y_true, num_classes)
    validator.validate_classes(y_pred, num_classes)

    if flatten:
        y_true = y_true.ravel()
        y_pred = y_pred.ravel()

    if library == 'sklearn':
        return sklearn_f1_score(y_true, y_pred, average='macro')

    if library == 'Moral88' or library is None:
        f1_per_class = []
        for cls in range(num_classes):
            tp = np.logical_and(y_pred == cls, y_true == cls).sum()
            fp = np.logical_and(y_pred == cls, y_true != cls).sum()
            fn = np.logical_and(y_pred != cls, y_true == cls).sum()

            f1 = (2 * tp) / (2 * tp + fp + fn) if (2 * tp + fp + fn) > 0 else 0
            f1_per_class.append(f1)

        mean_f1 = np.mean(f1_per_class)
        return f1_per_class, mean_f1

    raise ValueError("Unsupported library for F1 Score.")
