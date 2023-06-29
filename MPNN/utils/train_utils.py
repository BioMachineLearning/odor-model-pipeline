import torch

class EarlyStopper():

  def __init__(self, save_path, metric, patience):
    if metric in ['roc_auc', 'r2']:
      self.best_score = 0
      self.mode = 'higher'
    elif metric in ['rmse']:
      self.best_score = float('inf')
      self.mode = 'lower'
    else:
      raise ValueError('Unexpected metric: {}'.format(metric))

    self.save_path = save_path
    self.max_patience = patience
    self.patience_count = 0

  def __call__(self, model, current_score):
    from deepchem.models import TorchModel
    if self.mode == 'higher' and current_score > self.best_score:
      self.best_score = current_score
      self.patience_count = 0
      if type(model).__bases__[0] == TorchModel:
        torch.save(model.model.state_dict(), self.save_path + '/early_stop.pt')
      else:  # KerasModel
        model.model.save(self.save_path + '/early_stop')
    elif self.mode == 'lower' and current_score < self.best_score:
      self.best_score = current_score
      self.patience_count = 0
      if type(model).__bases__[0] == TorchModel:
        torch.save(model.model.state_dict(), self.save_path + '/early_stop.pt')
      else:  # KerasModel
        model.model.save(self.save_path + '/early_stop')
    else:
      self.patience_count += 1

    return self.patience_count == self.max_patience

  def load_state_dict(self, model):
    model.model.load_state_dict(torch.load(self.save_path + '/early_stop.pt'))

  def load_keras_model(self, model):
    model.restore(model_dir=self.save_path)
